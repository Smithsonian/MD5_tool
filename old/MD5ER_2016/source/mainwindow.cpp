#include "mainwindow.h"
#include "ui_mainwindow.h"


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{



    //qRegisterMetaType< std::string >("std::string");
    //qRegisterMetaType< std::vector<std::string> >("std::vector<std::string>");
    //qRegisterMetaType< unsigned long int >("unsigned long int");
    //qRegisterMetaType<QTextBlock>("QTextBlock");

    ui->setupUi(this);

    setAcceptDrops(true);
    //this->statusBar()->setSizeGripEnabled(false);
    //setWindowFlags(Qt::Dialog | Qt::MSWindowsFixedSizeDialogHint);
    //this->setFixedSize(this->maximumSize());
    this->setFixedSize(this->size());
    //ui->centralwidget->setFixedSize(this->size());
    //QSettings settings;
    //restoreGeometry(settings.value("mainWindowGeometry").toByteArray());
    //restoreState(settings.value("mainWindowState").toByteArray());



    //this->setAttribute(Qt::WA_NoSystemBackground, true);
    //this->setAttribute(Qt::WA_TranslucentBackground, true);

    //this->setWindowFlags(Qt::WindowStaysOnTopHint);



    //this->qstrFolderStorage = settings.value("qstrFolderStorage", "").toString();

    //ui->labelStorage->setText(this->qstrFolderStorage);

/*
    if (boost::filesystem::is_directory("/Volumes/RAMDisk/")){
        cout << "Ramdisk already exists" << endl;
    } else {
        //int res = system("diskutil erasevolume HFS+ 'RAMDisk' `hdiutil attach -nomount ram://2097152`"); //2097152 = 1Gb
        int res = system("diskutil erasevolume HFS+ 'RAMDisk' `hdiutil attach -nomount ram://4194303`"); //4194303 = 2Gb
        if (res){
            cout << "Error creating ramdisk" << endl;
        }
    }*/
}



void MainWindow::slotPopup(QString qstrMsg){
    //qDebug() << "slotPopup(" << qstrMsg << ")";
    QApplication::beep();

    QMessageBox messageBox;
    messageBox.critical(0, "Error", qstrMsg);
    messageBox.setFixedSize(600,200);
    messageBox.setWindowFlags(Qt::WindowStaysOnTopHint);
}

bool fileExists(QString path) {
    QFileInfo checkFile(path);
    // check if file exists and if yes: Is it really a file and no directory?
    if (checkFile.exists() && checkFile.isFile()) {
        return true;
    } else {
        return false;
    }
}



void MainWindow::slotResult(QString csvfile, QString filename, QString checksum){
    qDebug()<< "slotResult(" << filename << "," << checksum <<  ")";

        //@TODO (fstream on windows problem?)
    /*
    //bool file_exists = boost::filesystem::exists( csvfile.toStdString() );
    bool file_exists = fileExists(csvfile);
    ofstream myfile;
    myfile.open (csvfile.toStdString(), ios::out | ios::app);
    if (!file_exists){
        cout  << "Appending csv header.." << endl;
        //myfile << "Filename;Difference Original:LZW;Difference LZW:Decompressed;Difference Original:Decompressed\n";
        //myfile << "Checksum;File\n";
    }
    myfile << checksum.toStdString() << "  " << fileInfo.fileName().toStdString() << "\n";
    myfile.close();*/

    // QString filename = "Data.txt";
    QFile file(csvfile);
    if (file.open(QIODevice::ReadWrite | QIODevice::Append)) {
        QTextStream stream(&file);
        stream << checksum << "  " << QFileInfo(filename).fileName() << endl;
    }
    file.close();



}

void MainWindow::slotStatus(QString filename, double pct){
    //qDebug() << "slotStatus(" << filename << "," << pct << ")";

    ui->labelfilenow->setText(filename);

    if (round(pct)==100){
        ui->progressBar->setValue(0);
        ui->labelfilenow->setText("Done.");
    } else {
        ui->progressBar->setValue(pct);
    }
    QApplication::processEvents();
}

bool MainWindow::nameProcess(QString folderBox){
    qDebug()<<"nameProcess("<<folderBox<<")";

    int name_format_md5 = ui->comboBox_md5name->currentIndex();


    //Make the  worker
    QThread *thread = new QThread; //On the heap, make sure to destruct later
    worker *workerProcessor = new worker(name_format_md5);//predictor, rowsperstrip, repeat_times); //On the heap
    workerProcessor->moveToThread(thread);

    connect(this, SIGNAL( sigProcess(QString) ), workerProcessor, SLOT(slotProcess(QString) ));
    connect(workerProcessor, SIGNAL(sigPopup(QString)), this, SLOT(slotPopup(QString)) );
    connect(workerProcessor, SIGNAL(sigResult(QString, QString, QString)), this, SLOT(slotResult(QString, QString, QString)) );
    connect(workerProcessor, SIGNAL(sigStatus(QString, double)), this, SLOT(slotStatus(QString, double)));


    //Connect its own destruction
    connect(workerProcessor, SIGNAL(finished()), thread, SLOT(quit()));
    connect(workerProcessor, SIGNAL(finished()), workerProcessor, SLOT(deleteLater()));
    connect(thread, SIGNAL(finished()), thread, SLOT(deleteLater()));



    thread->start();

    emit sigProcess(folderBox);





    ui->labelfilenow->setText("");
    return true;
}




void MainWindow::dragEnterEvent(QDragEnterEvent *e){
    ui->progressBar->setValue(0);
    //ui->progressBar2->setValue(0);
    //ui->progressBar->setFormat("0%");
    //ui->progressBar2->setFormat("0%");
    if (e->mimeData()->hasUrls()) {
        e->acceptProposedAction();
    }
}


void MainWindow::on_pushButtonPickFolder_clicked(){
    qDebug()<< "on_pushButtonPickFolder_clicked()";
    QString dir = QFileDialog::getExistingDirectory(this, tr("Open Directory"),
                                             NULL,
                                             QFileDialog::ShowDirsOnly
                                             | QFileDialog::DontResolveSymlinks);
    qDebug() << " dir=" << dir;
    if (dir.size()!=0){
        runFolder(dir);
    } else {
        qDebug() << "String selection was empty. Ignoring.";
    }
}

void MainWindow::runFolder(QString foldername){
    qDebug() << "runFolder(" << foldername << ")";
    ui->statusBar->showMessage(foldername);

    QApplication::processEvents();

    bool ok=nameProcess(foldername);
    ui->labelfilenow->setText("");
    if (!ok){
        qDebug() << "nameProcess not ok. returning.";
        //ui->progressBar->setFormat("Error - see log");
        //ui->progressBar2->setFormat("");
        return;
    }
}

void MainWindow::dropEvent(QDropEvent *e){
    qDebug()<<"dropEvent()";

    QStringList folders;
    foreach (const QUrl &url, e->mimeData()->urls()) {
        folders << url.toLocalFile();
    }
    folders.sort();

    //int numboxes = folders.size();

    QString folder;
    foreach( folder, folders ){
        runFolder(folder);
    }
}


void MainWindow::closeEvent(QCloseEvent *event){
    qDebug()<< "closeEvent()";

    //Save window state
    QSettings settings;
    settings.setValue("mainWindowGeometry", saveGeometry());
    settings.setValue("mainWindowState", saveState());

}










MainWindow::~MainWindow()
{
    delete ui;
}


