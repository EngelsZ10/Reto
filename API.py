import face_recognition
from PIL import Image
import numpy as np
from io import BytesIO
import base64
from flask import Flask, jsonify, request, Response, render_template

app = Flask(__name__)

def crop_image(img, coordinates):
    top, right, bottom, left = coordinates
    box = (left, top, right, bottom)
    cropped_img = img.crop(box)
    return cropped_img



@app.route('/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"

@app.route('/pruebas', methods=['GET', 'POST'])
def pruebas():
    return Response(open('pruebas.html').read(), mimetype="text/html")


@app.route('/agregarUsuario', methods=['GET'])
def addUser():#/
    face = "data:image/JPEG;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQgJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCABrAGsDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDyHqcDmrNvp81wf7o96i0yM3Nxz0xniulBjtIC8nRRngcms6lRrY66dNNXZVtdAiYjzSznsM9a37Tw7CF3LZoPqKwoda1CKQSxWagdg6kmrcfi3WjlfIh+XsykEfhWDU31N4zhHodNDpYBGIUU+y1fXTiFwEUe4rmYPFWrtIm+GAKBztHWuo0rUnvroKSMEZx0K/WuecJI6o1Iy6D47ICLaVGfXFV5bFepjVvqK6JrcdFqvdqtvbmYr07Vimza67HNz6PayjMlpE31QVm3HhbTJRn7OYif+eZIq/P4pitnImt2b2Uc02Pxjosp2uJY2/24zW6VRbGEpUnujl7vwnt5t7o/7sozWPc6RfWp+eEsB3Tmu9uNZ0idMw3G49OBUJIdmQ4LDBZPQGto1qkfi1MHSpy+HQ87zjqMH0pc+1ddqGlwTBsoNx6HFcjIDHIyFeQcV1U6qktjkqUuRl/w7Dvkc46V1tnp63c0bSDMaHdtx1NYWiWj2bSxS8SByDXZ2irFbqwIHFcdWep10YaWZq2tpAqBWjQjuCOKnnGjMpWdLdseo5X8a4TVtdvftIihRnQHGSCFH+NUrpruKVcanM0ciBlaBNuxvTaBmpUHLdlyqKOyO0aDRd+2FogSehq1bi2tJxIqhc9dvQ1ylmkS6Z9pl1Is7SYWC4xnZ0zkdDnmr8d5G1uBFNuwencVnKDXU1hJNXsdxA4m5U0l8ivblHIGRg5rK0m6VU3M3Poadq18ojBzkdBWFtTV7GZNoNtO5IJOffgVA3gS1uvvz7R/dRRioru5nbbDG5kdhkRxsAT75PAFZmpSanpl6YlWFZNqMFaRvmDeje3fiummqj2ZzVORbnS2HgbTdPcTqZZJ1+67HofYVW1PwzIk4v4buQzhujYwR6GqVh4ou47NJ72N4bZnKLcFg8TsO2eCPyrpbfUEu4Rjg47cgj1B7ilKU4vUcYwktDm7i13Lu6HrzXC30YW+mG0/er1K9i+XIHBHevPNTtn/ALSnKqSC2RV0ZasivHRG1eKo1WYx4UMQfxxWhGzYA6kVklCt62RjPI/pW3axg7Ryc9qiT2NYq7ZZtrVGcMwBbPcZraS1h8sb4Isj1FV7W2A2sasSzRRryw+hqbsrl8jJv4YkJCIgHoBWRJ+8ddqKqjnIGM1sXbFwW2kL9KyZZNgBCnPpQNqxagLL8oPTripHfzoCnUd/rVS0YvkE8n0q2E2N14NQ1qWtUVUtLZ35hG8/eJJ5rTXw9YXkSGaAttBAHXGfrTYo1Zh046VpWsq52BgHHVavma2J5fIz5PDGmiExHc0eMBGPC/QU20tI9MHlW7OIx91M5A+lbjI0iHn6k9qqTW+RwDkVDm3uwjG2xWmn3xAE89a524tg1w7bCcnrW1KjIeR+VU2zuPSnF2JkjJubmK7ltrmIYDRhWHoQSK3bHHlpxz3PesfVYRbXca+SY85bpw3TOPxzmr1lKfLBJ9q0ktETTerNlHfGzOB2pnlMzBiSSPWlg+bAB4PX1q0qgjJwKzR0mfOgKEknA61zyGe8uCI1+QHr7V0t/jy3jQY9ayridtN02M2NibmZuCobFVF9iJK+4tpZTFsIjYHerUtvPEp3ISB3xWvpF55duFnj2SdSh5xVPX/EDacsHlWEt0kj7WZMBV+pqW23oVokU7adZ0LBSHXgg1Z2B3EmAHHUilnEDRRXMaGMyAZB461PbpgDj6mpuNKxPbyyAbTyPWrQO4nJGR0qFNoUsOvfA60jzfKCFxnqD1qQsVL5ABkcCsp1XdyefpWjdybo1HU96rxyxogVkBPrgf41a2MnuaPjjw/rNtYpfah5IhhcRpsfONx5xx3OPyrlbN8AqM8CvbviLafa/A2o4GTCFm4/2GBP6A14dGvoTjFdVWKizjw03JXOhtZRsX9TUrXcSYBPHrWQk7Ih68DkVFGzzuQCSO3Nctju5i/c3ZIzyB2rDlmk+0K8TMMNyO1aF2hjVizHOMACqKWlxM+5nWJO2eTVwIleWx0EV2Wjw8eWxnI6VFfajNFbBUUA9SPvCs6Rb0AJBPG698qRVhLO7liH7+NiOxyKVral2nYdb3LXMgeUksPyFbFtMu3YTzWHBBNHP5bIUfpg96v7JUYADHvUSVwjPua+5SnH6VTuBlwwbIot5iVwwwRQ7ZbAFQkU2V5RuHv1qL/hGp7tVuAjP5ihtwjY549qnlzt6jPSu08MeJUs/DtpbykFowy5J7bjj9MV0U4qW5y1pW2R315ax3tlPayjMc0bRsPUEYNfOSW7288ltJ9+F2ib6qcV9J18661+48VaxF3W8kP5tn+tdddaI4cK7SaKrRlpdo6fzrRs4Fh5YdDkVTDc7u1WlbIA6e9cLPTRS1XUUjlXdCQnZwOKrx6nhR5UDv6kkCtWe1jnjEbDIb1FV47CO3kUY4960i421NIXuQG+kgUyixlYMcHB6U9NY2N8ttNirk6wMQpfA9KelpbbRscE1TaOmysRtrFsm15G+QdVKnitSC4guod0TDB55GKy5tLW42mToDwvY/WrtvEIFVV7DmsZuPQ5paskEbbiRT48NIMjGalWU4OR+VQt+5QkHJPT2qBEd2QHx0wP1qgZnjJUEgCrUmXOTVGct5zY6cfyrWLsYzVz6Kr538XoV8da0Bx/pGfzVT/Wvoivn7xmB/wn2sf9dk/9FrXdX2R5uG+JmTHISMD7w6irUc4CnjJxWe/y3QI4JHNTxE7/AKnFcUlY9CMrlr7Y6k7Dkg96ui7iZAXALY+73rOi+4R6imRAG9dT0A4FTy3Nb2L02ZSx8tQM4AqezaJJMOqhh0HrUSsdic9W5pZVXbuxz60S1Q0zRZ40GQQQf0qPzAzYGKr4ATIqSMnIrPYtssdFxmoZW3EKBTSTubnvRFy7E9TTW1yL62I59yLx61DtUk5POat3Hb61S704sUlof//Z"
    naciones = [
    "Afganistán",
    "Albania",
    "Alemania",
    "Andorra",
    "Angola",
    "Anguila",
    "Antigua y Barbuda",
    "Aotearoa Nueva Zelanda",
    "Arabia Saudí",
    "Argelia",
    "Argentina",
    "Armenia",
    "Aruba",
    "Australia",
    "Austria",
    "Azerbaiyán",
    "Bahamas",
    "Bahréin",
    "Bangladesh",
    "Barbados",
    "Bélgica",
    "Belice",
    "Benín",
    "Bermudas",
    "Bielorrusia",
    "Bolivia",
    "Bosnia y Herzegovina",
    "Botsuana",
    "Brasil",
    "Brunéi Darussalam",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Bután",
    "Cabo Verde",
    "Camboya",
    "Camerún",
    "Canadá",
    "Chad",
    "Chile",
    "China Taipei",
    "Chipre",
    "Colombia",
    "Comoras",
    "Congo",
    "Costa de Marfil",
    "Costa Rica",
    "Croacia",
    "Cuba",
    "Curazao",
    "Dinamarca",
    "Dominica",
    "Ecuador",
    "Estados Unidos de América",
    "Egipto",
    "El Salvador",
    "Emiratos Árabes Unidos",
    "Eritrea",
    "Escocia",
    "Eslovaquia",
    "Eslovenia",
    "España",
    "Estonia",
    "Esuatini",
    "Etiopía",
    "Filipinas",
    "Finlandia",
    "Fiyi",
    "Francia",
    "Gabón",
    "Gales",
    "Gambia",
    "Georgia",
    "Ghana",
    "Gibraltar",
    "Granada",
    "Grecia",
    "Guam",
    "Guatemala",
    "Guinea",
    "Guinea Ecuatorial",
    "Guinea-Bissáu",
    "Guyana",
    "Haití",
    "Honduras",
    "Hong Kong, China",
    "Hungría",
    "India",
    "Indonesia",
    "Inglaterra",
    "Irak",
    "Irlanda del Norte",
    "Islandia",
    "Islas Caimán",
    "Islas Cook",
    "Islas Feroe",
    "Islas Salomón",
    "Islas Vírgenes Británicas",
    "Islas Vírgenes Estadounidenses",
    "Israel",
    "Italia",
    "Jamaica",
    "Japón",
    "Jordania",
    "Kazajstán",
    "Kenia",
    "Kosovo",
    "Kuwait",
    "Laos",
    "Lesoto",
    "Letonia",
    "Líbano",
    "Liberia",
    "Libia",
    "Liechtenstein",
    "Lituania",
    "Luxemburgo",
    "Macao",
    "Macedonia del Norte",
    "Madagascar",
    "Malasia",
    "Malaui",
    "Maldivas",
    "Mali",
    "Malta",
    "Marruecos",
    "Mauricio",
    "Mauritania",
    "México",
    "Moldavia",
    "Mongolia",
    "Montenegro",
    "Montserrat",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nepal",
    "Nicaragua",
    "Níger",
    "Nigeria",
    "Noruega",
    "Nueva Caledonia",
    "Omán",
    "Países Bajos",
    "Pakistán",
    "Palestina",
    "Panamá",
    "Papúa Nueva Guinea",
    "Paraguay",
    "Perú",
    "Polonia",
    "Portugal",
    "Puerto Rico",
    "Qatar",
    "RD del Congo",
    "RDP de Corea",
    "República Centroafricana",
    "República Checa",
    "República de Corea",
    "República de Irlanda",
    "República Dominicana",
    "República Kirguisa",
    "Irán",
    "China",
    "Ruanda",
    "Rumanía",
    "Rusia",
    "Samoa",
    "Samoa Estadounidense",
    "San Cristóbal y Nieves",
    "San Marino",
    "San Vicente y las Granadinas",
    "Santa Lucía",
    "Santo Tomé y Príncipe",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leona",
    "Singapur",
    "Siria",
    "Somalia",
    "Sri Lanka",
    "Sudáfrica",
    "Sudán",
    "Sudán del Sur",
    "Suecia",
    "Suiza",
    "Surinam",
    "Tahití",
    "Tailandia",
    "Tanzania",
    "Tayikistán",
    "Timor Oriental",
    "Togo",
    "Tonga",
    "Trinidad y Tobago",
    "Túnez",
    "Turcas y Caicos",
    "Turkmenistán",
    "Turquía",
    "Ucrania",
    "Uganda",
    "Uruguay",
    "Uzbekistán",
    "Vanuatu",
    "Venezuela",
    "Vietnam",
    "Yemen",
    "Yibuti",
    "Zambia",
    "Zimbabue"
]
    return render_template("index.html", naciones = naciones, face=face)

@app.route('/get_encoding', methods=['POST'])
def getEncodings():
    image = Image.open(request.files["img"])
    load = np.array(image)
    face_locations = face_recognition.face_locations(load)
    result = []
    for i in face_locations:
        cropped_img = crop_image(image, i)
        load = np.array(cropped_img)
        try:
            encoding = list(face_recognition.face_encodings(load)[0])
        except:
            continue
        img_byte_array = BytesIO()
        cropped_img.save(img_byte_array, format="JPEG")
        base64_image = base64.b64encode(img_byte_array.getvalue())
        result.append({"face":'data:image/JPEG;base64,' + str(base64_image)[2:-1], "encoding":encoding})
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=105, debug=True)