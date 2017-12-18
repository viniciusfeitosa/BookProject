package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/codegangsta/negroni"
	"github.com/gorilla/mux"
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"github.com/viniciusfeitosa/BookProject/UsersService/user_service/server"

	"git.apache.org/thrift.git/lib/go/thrift"
)

// App is the struct with app configuration values
type App struct {
	DB     *sqlx.DB
	Router *mux.Router
	Cache  Cache
}

// Initialize create the DB connection and prepare all the routes
func (a *App) Initialize(cache Cache, db *sqlx.DB) {
	a.DB = db

	a.Cache = cache
	a.Router = mux.NewRouter()
	a.initializeRoutes()
}

func (a *App) initializeRoutes() {
	a.Router.HandleFunc("/users", a.getUsers).Methods("GET")
	a.Router.HandleFunc("/user", a.createUser).Methods("POST")
	a.Router.HandleFunc("/user/{id:[0-9]+}", a.getUser).Methods("GET")
	a.Router.HandleFunc("/user/{id:[0-9]+}", a.updateUser).Methods("PUT")
	a.Router.HandleFunc("/user/{id:[0-9]+}", a.deleteUser).Methods("DELETE")
}

// Run initialize the server
func (a *App) Run(addr string) {
	n := negroni.Classic()
	n.UseHandler(a.Router)
	log.Fatal(http.ListenAndServe(addr, n))
}

func (a *App) getUser(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id, err := strconv.Atoi(vars["id"])
	if err != nil {
		respondWithError(w, http.StatusBadRequest, "Invalid product ID")
		return
	}

	if value, err := a.getUserFromCache(id); err == nil {
		log.Println("from cache")
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(value))
		return
	}

	user, err := a.getUserFromDB(id)
	if err != nil {
		switch err {
		case sql.ErrNoRows:
			respondWithError(w, http.StatusNotFound, "User not found")
		default:
			respondWithError(w, http.StatusInternalServerError, err.Error())
		}
		return
	}

	response, _ := json.Marshal(user)
	if err := a.Cache.setValue(user.ID, response); err != nil {
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write(response)
}

func (a *App) getUsers(w http.ResponseWriter, r *http.Request) {
	count, _ := strconv.Atoi(r.FormValue("count"))
	start, _ := strconv.Atoi(r.FormValue("start"))

	if count > 10 || count < 1 {
		count = 10
	}
	if start < 0 {
		start = 0
	}

	users, err := list(a.DB, start, count)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithJSON(w, http.StatusOK, users)
}

func (a *App) createUser(w http.ResponseWriter, r *http.Request) {
	var user User
	decoder := json.NewDecoder(r.Body)
	if err := decoder.Decode(&user); err != nil {
		respondWithError(w, http.StatusBadRequest, "Invalid request payload")
		return
	}
	defer r.Body.Close()

	a.DB.Get(&user.ID, "SELECT nextval('users_id_seq')")
	JSONByte, _ := json.Marshal(user)
	if err := a.Cache.setValue(user.ID, string(JSONByte)); err != nil {
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	if err := a.Cache.enqueueValue(createUsersQueue, user.ID); err != nil {
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithJSON(w, http.StatusCreated, user)
}

func (a *App) updateUser(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id, err := strconv.Atoi(vars["id"])
	if err != nil {
		respondWithError(w, http.StatusBadRequest, "Invalid product ID")
		return
	}

	var user User
	decoder := json.NewDecoder(r.Body)
	if err := decoder.Decode(&user); err != nil {
		respondWithError(w, http.StatusBadRequest, "Invalid resquest payload")
		return
	}
	defer r.Body.Close()
	user.ID = id

	if err := user.update(a.DB); err != nil {
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithJSON(w, http.StatusOK, user)
}

func (a *App) deleteUser(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id, err := strconv.Atoi(vars["id"])
	if err != nil {
		respondWithError(w, http.StatusBadRequest, "Invalid User ID")
		return
	}

	user := User{ID: id}
	if err := user.delete(a.DB); err != nil {
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithJSON(w, http.StatusOK, map[string]string{"result": "success"})
}

func (a *App) getUserFromCache(id int) (string, error) {
	if value, err := a.Cache.getValue(id); err == nil && len(value) != 0 {
		return value, err
	}
	return "", errors.New("Not Found")
}

func (a *App) getUserFromDB(id int) (User, error) {
	user := User{ID: id}
	if err := user.get(a.DB); err != nil {
		switch err {
		case sql.ErrNoRows:
			return user, err
		default:
			return user, err
		}
	}
	return user, nil
}

func (a *App) runThriftServer(networkAddr string) {
	transportFactory := thrift.NewTFramedTransportFactory(thrift.NewTTransportFactory())
	protocolFactory := thrift.NewTBinaryProtocolFactoryDefault()
	serverTransport, err := thrift.NewTServerSocket(networkAddr)
	if err != nil {
		fmt.Println("Error!", err)
		os.Exit(1)
	}

	handler := &userHandler{app: a}
	processor := server.NewGetUserDataProcessor(handler)

	server := thrift.NewTSimpleServer4(processor, serverTransport, transportFactory, protocolFactory)
	fmt.Println("thrift server in", networkAddr)
	server.Serve()
}

type userHandler struct {
	app *App
}

func (handler *userHandler) GetUser(ctx context.Context, id int32) (*server.User, error) {
	var user User
	var err error
	userServer := &server.User{}
	if value, err := handler.app.getUserFromCache(int(id)); err == nil {
		if err = json.Unmarshal([]byte(value), &user); err != nil {
			return userServer, err
		}
		userServer.ID = int32(user.ID)
		userServer.Email = user.Email
		userServer.Name = user.Name
		return userServer, err
	}

	if user, err = handler.app.getUserFromDB(int(id)); err == nil {
		userServer.ID = int32(user.ID)
		userServer.Email = user.Email
		userServer.Name = user.Name
		return userServer, err
	}
	return userServer, err
}

func respondWithError(w http.ResponseWriter, code int, message string) {
	respondWithJSON(w, code, map[string]string{"error": message})
}

func respondWithJSON(w http.ResponseWriter, code int, payload interface{}) {
	response, _ := json.Marshal(payload)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	w.Write(response)
}
