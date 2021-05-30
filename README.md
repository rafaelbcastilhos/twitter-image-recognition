# twitter-image-recognition
Reconhecimento de imagens utilizando a API do Twitter e Visão Computacional da Azure

Twitter Streaming e Vision API:
- Streaming de um único usuário:
1. Quando submetido um novo post contendo uma foto. Exemplo

2. É realizado a extração do conteúdo enviando para a API Vision da Azure, obtendo como saída:
User: b0tney
Text: https://t.co/wNy3CxQ3Fa
URL:  http://pbs.twimg.com/media/E2kfBgWXoAcTkjr.jpg
['Neymar', 'Alisson Becker']
Description:  Alisson Becker, Neymar playing football

- Streaming de vários usuários:
1. Extraído o id do perfil de cada celebridade contida na lista
2. Busca por submissões de novos posts contendo uma foto
3. Realizado a extração do conteúdo enviando para a API Vision da Azure, obtendo a saída e registrando no arquivo tweets.json