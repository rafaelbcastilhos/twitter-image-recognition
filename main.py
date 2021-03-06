# -*- coding: utf-8 -*-
# Declaração de chaves para autenticação com Twitter
import tweepy as tw
from decouple import config

consumer_key = config('CONSUMER_KEY')
consumer_secret = config('CONSUMER_SECRET')
access_token = config('ACCESS_TOKEN')
access_token_secret = config('ACCESS_TOKEN_SECRET')

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

# Pesquisa por fotos postadas por celebridades
celebrities = ['cauareymond', 'aguiarthur', 'ivetesangalo', 'ClaudiaLeitte', 'neymarjr', 'BruMarquezine',
               'mariruybarbosa', 'FePaesLeme', 'Tatawerneck', 'FlaviaAleReal', 'julianapaes', 'dedesecco',
               'SabrinaSato', 'ahickmann', 'gusttavo_lima', 'Anitta']

for celebrity in celebrities:
    tweets = tw.Cursor(
        api.search,
        q=celebrity,
        since='2019-01-01').items(20)
    print('Celebrity: ', celebrity)
    print('Imagens postadas:')

    for tweet in tweets:
        if 'media' in tweet.entities:
            print(tweet.entities['media'][0]['media_url'])

    print('-----')
    print('\n')


# Streaming track
class StreamListenerTrack(tw.StreamListener):
    @staticmethod
    def on_status(status):
        print(status.user.screen_name)
        print(status.text)
        print('-----\n')


stream_track = tw.Stream(auth=auth, listener=StreamListenerTrack())
stream_track.filter(track=celebrities)

# Configurando API Vision Azure
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import json

credentials = CognitiveServicesCredentials(config('AZURE_CREDENTIAL'))
client = ComputerVisionClient("https://vision-twitter.cognitiveservices.azure.com/", credentials)


# Análise de uma imagem, identificando as pessoas envolvidas, descrevendo a ação e exibindo a confiança
class StreamListenerFollow(tw.StreamListener):

    @staticmethod
    def on_status(status):
        print("User:", status.user.screen_name)
        print("Text:", status.text)

        if 'media' in status.entities:
            url = status.entities['media'][0]['media_url']
            print("URL: ", url)

            analyze_celebrities = client.analyze_image_by_domain("celebrities", url, "en")
            celebrities_list = [celebridade['name'] for celebridade in analyze_celebrities.result["celebrities"]]
            print(celebrities_list)

            action_description = client.describe_image(url, 1, "en")
            text_description = action_description.captions[0].text
            print("Description: ", text_description)

            resultados = {
                'user': status.user.screen_name,
                'text': status.text,
                'url': url,
                'celebrity': celebrities_list,
                'description': text_description
            }

            with open('tweets.json', 'a') as out:
                out.write(json.dumps(resultados))
                out.write('\n')

        print('-----\n')


# Seguir novas publicações de um usuário
stream_follow = tw.Stream(auth=auth, listener=StreamListenerFollow())
stream_follow.filter(follow=['1297260503866146816'])

# Seguir novas publicações das celebridades e realizar reconhecimento das imagens
celebrities_id = []

for celebrity in celebrities:
    celebrity_id = api.get_user(celebrity).id_str
    celebrities_id.append(celebrity_id)

stream_follow_celebrities = tw.Stream(auth=auth, listener=StreamListenerFollow())
stream_follow_celebrities.filter(follow=celebrities_id)
