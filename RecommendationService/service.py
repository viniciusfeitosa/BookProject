from nameko.events import event_handler


class RecommendationHandler:
    name = 'recommendation_handler'

    @event_handler('news_user', 'news_label')
    def news_labels_to_user(self, data):
        pass
