#include "mainwindow.h"
#include <QApplication>
#include <QWidget>
#include <QThread>
#include <QMutex>
#include <QString>
#include <QtGui>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    return a.exec();
}
