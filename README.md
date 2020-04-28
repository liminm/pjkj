### Storage Setup

## How to setup Docker the first time
`
sudo docker pull mongo  // just download the image
sudo docker run --name mongoDB -p 27017:27017 -d mongo // run the image
`

After that MongoDB will run and not shutdown if its not explicitly told so, even after a restart it will automatically start again

To get an overview over all running container type
`
sudo docker ps 
`


## How to use the dictionary
`
# how to connect to the storage module
from storage.DatabaseDictionary import DatabaseDictionary

storage = DatabaseDictionary()


# how to save something
key = 'insert your key here'
game = {
    'player1': 'Lorenz',
    'player2': 'Matthias',
    'history': [
        {'FEN': '8/123/8a...', 'time_player': 1, ...},
        {'FEN': '8/123/8a...', 'time_player': 1, ...},
        ...
    ]
}

# how to read something
storage[key] = game
`

