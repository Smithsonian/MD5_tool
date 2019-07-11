#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QApplication>
#include <QWidget>
#include <QString>
#include <QtGui>
#include <QDebug>
#include <QMainWindow>
#include <QDebug>
#include <QThread>
#include <QDrag>
#include <QDragEnterEvent>
#include <QMimeData>
#include <QDir>
#include <QApplication>
#include <QMessageBox>
#include <QFileDialog>
#include <QFileSystemModel>
#include <QFileInfo>
#include <QSettings>

#include <fstream>
#include <iostream>

//#ifdef Q_WS_WIN
//    #include <tchar.h>
//    #include <windows.h>
//#endif

#include <string>

#include "worker.h"


namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
        std::string strSoftwareDate, strSoftwareRev;

    private:
        Ui::MainWindow *ui;

        QString qstrFolderStorage;

        std::string ssystem (const char *command);
        bool nameProcess(QString folderBox);
        void dragEnterEvent(QDragEnterEvent *e);
        void dropEvent(QDropEvent *e);

        void runFolder(QString);
    protected:
        void closeEvent(QCloseEvent *event);

    public slots:
        //void on_actionFull_Screen_triggered();
        //void on_actionSelect_Storage_triggered();
        void slotPopup(QString);
        void on_pushButtonPickFolder_clicked();

        //From Worker:
        void slotResult(QString, QString, QString);
        void slotStatus(QString, double);
    signals:
        //To Worker:
        void sigProcess(QString);


};

#endif // MAINWINDOW_H
