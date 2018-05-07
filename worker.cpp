
#include "worker.h"


using namespace std;




worker::worker(int _name_format_md5){//int _predictor, int _rowsperstrip, int _repeat_times){
	cout << "worker::worker()" << endl;
	this->name_format_md5 = _name_format_md5;
	//this->predictor = _predictor;
	//this->rowsperstrip = _rowsperstrip;
	//this->repeat_times = _repeat_times;
}

worker::~worker(){
	cout << "worker::~worker()" << endl;
}
/*
const std::string md5_from_file(const std::string& path)
{
    unsigned char result[MD5_DIGEST_LENGTH];
    boost::iostreams::mapped_file_source src(path);
    MD5((unsigned char*)src.data(), src.size(), result);

    std::ostringstream sout;
    sout<<std::hex<<std::setfill('0');
    for(auto c: result) sout<<std::setw(2)<<(int)c;

    return sout.str();
}*/

// QString md5_from_file(QString path){
//     QString qstr_checksum;
//     QFile file(path);
//     if (file.open(QIODevice::ReadOnly)) {
//         QByteArray fileData = file.readAll();
//         QByteArray hashData = QCryptographicHash::hash(fileData, QCryptographicHash::Md5);
//         qstr_checksum= hashData.toHex();
//     } else {
//         qDebug()<<"md5_fromfile("<<path<<") : opening file failed?!.";
//     }
//     qDebug()<<"md5_from_file("<<path<<")="<<qstr_checksum;
//     return qstr_checksum;
// }

QString md5_from_file(QString path){
    QString qstr_checksum;
    QCryptographicHash hash(QCryptographicHash::Md5);     
    QFile file(path);
    if (file.open(QIODevice::ReadOnly)) {
        if ( hash.addData(&file) ){
            qstr_checksum = hash.result().toHex();
        }
    } else {
        qDebug()<<"md5_fromfile("<<path<<") : opening file failed?!.";
    }
    qDebug()<<"md5_from_file("<<path<<")="<<qstr_checksum;
    return qstr_checksum;
}




void worker::slotProcess(QString folderBox) {
    qDebug()<<"slotProcess("<< folderBox << ")";
	
    #ifdef Q_WS_WIN
        QString qstr_native_slash("\\");
        char c_native_seperator = '\\';
    #else
        QString qstr_native_slash = "/";
        const char c_native_seperator = '/';
    #endif

	//Remove last "/" if applicable
    if (folderBox.length()>1 && folderBox[folderBox.length()-1]==QChar(c_native_seperator)){
		folderBox = folderBox.remove(folderBox.length()-1,1);
	}
	

	QDir folderDir(folderBox);
	QStringList fileFilter;/*
	fileFilter << "*.tif" << "*.tiff" << "*.TIF" << "*.TIFF"
	<< "*.png" << "*.PNG" << "*.iiq" << "*.IIQ"
	<< "*.cr2" << "*.nef" << "*.NEF" << "*.CR2"
	<< "*.MOS" << "*.mos" << "*.bmp" << "*.CR2"
	<< "*.jpg" << "*.jpeg" << "*.JPEG" << "*.JPG";*/
	QStringList listFiles = folderDir.entryList(fileFilter, QDir::NoDotAndDotDot | QDir::Files);
    //qDebug() << listFiles;


    QStringList parent_folders = folderBox.split( qstr_native_slash );

	QString csvname = "md5.md5";
	if (name_format_md5==1){ //(folder).md5
		if (parent_folders.length()>0){
			csvname = parent_folders.value( parent_folders.length() - 1 ) + ".md5";
		}
	} else if (name_format_md5==2){ //(parent_folder)-(folder).md5
		if (parent_folders.length()>1){
			csvname = parent_folders.value( parent_folders.length() - 2 ) + "-" + parent_folders.value( parent_folders.length() - 1 ) + ".md5";
		}
	}
	
    QString csvfile = folderBox + qstr_native_slash + csvname;


	int numfiles = listFiles.size();
	//int k=0;
	for (int i=0; i<numfiles; i++){	
		//if (QString::compare(listFiles[i], csvname, Qt::CaseInsensitive)==0){
		if (listFiles[i].contains(".md5")){
			continue;
		}
        QString fname = folderBox + qstr_native_slash + listFiles[i];
        emit sigStatus(fname, (double(i)/double(numfiles))*100);
        //qDebug() << "fname=" << fname;
        // std::string checksum = md5_from_file(fname.toStdString());
        QString qstr_checksum = md5_from_file(fname);
        emit sigResult(csvfile, fname, qstr_checksum);
	}
	emit sigStatus(folderBox, 100);
	emit finished();
}



