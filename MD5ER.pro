#-------------------------------------------------
#
# Project created by QtCreator 2016-04-04T23:22:25
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = MD5ER
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    worker.cpp

HEADERS  += mainwindow.h \
    worker.h

FORMS    += mainwindow.ui


CONFIG += static
static {
    CONFIG += static
    #QTPLUGIN += qsqloci qgif
    DEFINES += STATIC
    message("Static build.")
}

RESOURCES += \
    images.qrc
