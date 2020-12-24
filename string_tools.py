import re
import datetime


def month_to_int(text):                                                                                                 # function to convert (french) months and day to date
    if "janvier" in text:
        text = re.sub('janvier', '01', text)
    elif 'février' in text:
        text = re.sub('février', '02', text)
    elif 'mars' in text:
        text = re.sub('mars', '03', text)
    elif 'avril' in text:
        text = re.sub('avril', '04', text)
    elif 'mai' in text:
        text = re.sub('mai', '05', text)
    elif 'juin' in text:
        text = re.sub('juin', '06', text)
    elif 'juillet' in text:
        text = re.sub('juillet', '07', text)
    elif 'août' in text:
        text = re.sub('août', '08', text)
    elif 'septembre' in text:
        text = re.sub('septembre', '09', text)
    elif 'octobre' in text:
        text = re.sub('octobre', '10', text)
    elif 'novembre' in text:
        text = re.sub('novembre', '11', text)
    elif 'décembre' in text:
        text = re.sub('décembre', '12', text)
    text = re.sub('lundi', '', text)
    text = re.sub('mardi', '', text)
    text = re.sub('mercredi', '', text)
    text = re.sub('jeudi', '', text)
    text = re.sub('vendredi', '', text)
    text = re.sub('samedi', '', text)
    text = re.sub('dimanche', '', text)
    text = text[1:]
    return text


# dobbiamo cercare: Date, Distance, Dénivelé


def format_text(data):                                                                                                  # used to estrapolate informations about a race
    date, distance, elevation = 0, 0, 0
    output = []
    for line in data.split("\n"):
        if "Date" in line:
            date = re.sub('Date : ', '', line)
            date = month_to_int(date)
            date = re.sub(' ', '-', date)
        if "Distance" in line:
            distance = re.sub('Distance : ', '', line)
            distance = re.sub(' kms', '', distance)
        if "Dénivelé" in line:
            elevation = re.sub('Dénivelé : ', '', line)
            elevation = re.sub(' m', '', elevation)
    if date: output.append(date)
    if distance: output.append(distance)
    if elevation: output.append(elevation)
    return output


def date_format(date):                                                                                                  # change date format
    d = datetime.datetime.strptime(date, '%d-%m-%Y')
    return datetime.date.strftime(d, "%Y-%m-%d")


def format_time(text):                                                                                                  # change format time
    char1 = "\ "
    text = re.sub(char1, '', text)
    char2 = "''"
    text = re.sub(char2, 'sec', text)
    char3 = "'"
    text = re.sub(char3, 'min', text)
    try:
        hour = int(text.split("h")[0])
        text = re.sub(str(hour) + 'h', '', text)
    except ValueError:
        hour = 0
    minute = int(text.split('min')[0])
    text = re.sub(str(minute) + 'min', '', text)
    second = int(text.split("sec")[0])
    text = re.sub(str(second) + "sec", '', text)
    total = int(hour * 3600 + minute * 60 + second)
    return total                                                                                                        # the value total is expressed in seconds (this is the value that is gonna be stored in the DB)
