/****************************************************************************
**
** Copyright (C) 2015 Tim Zaman.
** Contact: http://www.timzaman.com/ , timbobel@gmail.com
**
**
****************************************************************************/

#ifndef WORKER_H
#define WORKER_H

#include <QApplication>
#include <QObject>
#include <QThread>
#include <QMutex>
#include <QString>
#include <QFile>
#include <QIODevice>
#include <QDir>
#include <QDebug>

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

// MD5 Stuff
#include <QCryptographicHash>
//#include <openssl/md5.h>






class worker : public QObject{
	Q_OBJECT


	 
	public:
		worker(int);//int, int, int);
		~worker();


	private:
		//bool writeTIFF(std::string sFilename, int);

		//int predictor;
		//int rowsperstrip;
		//int repeat_times;
		int name_format_md5;
	public slots: 
        void slotProcess(QString);

	signals:
        void sigPopup(QString);
		void sigStatus(QString, double);
		void sigResult(QString, QString, QString);
		void finished();

};

#endif





