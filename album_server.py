from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        len_ = len(album_names)
        result = "Количество альбомов: {}".format(len_)
        result += ", Список альбомов {}: ".format(artist)
        result += ", ".join(album_names)
       
        
    return result
def save_album(album):
    session = connect_db()
    session.add(album)
    session.commit()
    print("Спасибо, данные сохранены!")

@route("/albums", method="POST")
def album_post():
    album_data = {
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album"),
        "year": request.forms.get("year")
    }
    if len(album_data["year"]) != 4: 
        return  "Ошибочный год"
    elif (album_data["year"][0:2] in ["19","20"])==False:
        return  "Ошибочный год"
    elif (int(album_data["year"]) > 2021):
        return  "Ошибочный год"         
            
    else: 
        album.save_album(album_data)

        return "Данные успешно сохранены"


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)