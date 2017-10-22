package main

import (
	"fmt"
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"log"
	"os"
)

const tableCreationQuery = `CREATE TABLE IF NOT EXISTS users
(
id SERIAL,
name TEXT NOT NULL,
email TEXT NOT NULL,
password TEXT NOT NULL,
CONSTRAINT users_pkey PRIMARY KEY (id)
)`

func main() {
	connections := []string{
		os.Getenv("DATABASE_TEST_URL"),
		os.Getenv("DATABASE_DEV_URL"),
		os.Getenv("DATABASE_URL"),
	}
	fmt.Println("Starting User migration")
	for _, connection := range connections {
		db, err := sqlx.Open("postgres", connection)
		if err != nil {
			log.Fatal(err)
		}
		if _, err = db.Exec(tableCreationQuery); err != nil {
			log.Fatal(err)
		}
	}
	fmt.Println("Finished User migration")
}
