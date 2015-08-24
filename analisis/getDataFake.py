#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import os
import config
import MySQLdb
import random

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# Schema reflection! Para que las clases esten
# Actualizadas con las migraciones de la DB
Base = automap_base()
# Base = declarative_base()

db_url = config.db_url
engine = create_engine(db_url)

# reflect the tables
Base.prepare(engine, reflect=True)

Historical = Base.classes.historical
Anomaly = Base.classes.anomaly
SegmentSnapshot = Base.classes.segment_snapshot
Causa = Base.classes.causa

session = Session(engine)


def readSegmentos():
    """
            readSegmentos()
    """
    result = []

    try:
        db = MySQLdb.connect(host=config.mysql["host"], passwd=config.mysql[
                             "password"], user=config.mysql["user"])
        db.select_db("dashboardoperativo")
        cur = db.cursor()
    except Exception, ex:
        print ex
        result = []
    else:
        cur.execute("SELECT * FROM segment_snapshot")
        for row in cur.fetchall():
            result.append(row)
    finally:
        cur.close()
        db.close()
        return result


def createSegmentos():

    db = MySQLdb.connect(host=config.mysql["host"], passwd=config.mysql[
                         "password"], user=config.mysql["user"])
    cur = db.cursor()
    db.select_db(config.mysql["db"])

    causas = ["Choque", "Manifestacion", "Animales sueltos"]

    try:
        for ID in range(10, 58):
            cur.execute("""INSERT INTO segment_snapshot VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (ID, time.strftime('%Y-%m-%d %H:%M:%S'), random.randrange(5, 21),
                         random.randrange(0, 101), causas[random.randrange(0, 3)], random.randrange(
                             0, 21), random.randrange(1, 120),
                         random.random(), random.randrange(0, 4)))
            print "Auto Increment ID: %s" % ID
    except Exception, ex:
        print(ex)
    finally:
        cur.close()
        db.commit()
        db.close()


def getData():

    filecorredorfake = os.path.abspath("analisis/corredores_fake.json")
    with open(filecorredorfake) as f:
        output = json.loads(f.read())

    return output


def parserEmitDataFake(self, result):
    """
      funcion que trae los datos de mongo, crea un json y emite al front segun corredor
    """
    corredores = ["independencia", "Illia", "nueve_de_julio", "alem", "corrientes",
                  "rivadavia", "av_de_mayo", "san_martin", "juan_b_justo", "cordoba", "paseo_colon", "cabildo", "pueyrredon", "alcorta", "libertador"]

    if len(result):
        for i in range(len(corredores)):
            self.emit(corredores[i], result['corredores'][
                      i][result['corredores'][i].keys()[0]])
            time.sleep(0.5)
    else:
        self.emit('info', "sin datos")


def updateSegmentos():

    db = MySQLdb.connect(host=config.mysql["host"], passwd=config.mysql[
                         "password"], user=config.mysql["user"])
    causas = ["Choque", "Manifestacion", "Animales sueltos"]
    query = """UPDATE segment_snapshot SET timestamp_medicion = %s, tiempo = %s, velocidad = %s, causa = %s, causa_id = %s, duracion_anomalia = %s, \
  indicador_anomalia =%s, anomalia = %s WHERE id = %s"""
    db.select_db(config.mysql["db"])

    cur = db.cursor()
    for ID in range(1, 57):
        # timestamp_medicion, tiempo, velocidad, causa, causa_id, duracion_anomalia, indicador_anomalia, anomalia, id
        update = (time.strftime('%Y-%m-%d %H:%M:%S'), random.randrange(5, 21), random.randrange(0, 101), causas[random.randrange(0, 3)],
                  random.randrange(0, 21), random.randrange(1, 120),
                  random.random(), random.randrange(0, 4), ID)
        print update
        cur.execute(query, update)

    cur.close()
    db.commit()
    db.close()


if __name__ == '__main__':
    createSegmentos()

    while(True):
        updateSegmentos()
        print("Generando nuevos datos")
        time.sleep(60)
