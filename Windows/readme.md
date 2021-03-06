# MD5_tool

8 Oct 2019

 * md5tool.exe - Executable script for Windows 10 64-bit, version 0.1.2

## How to use

On Windows, double click the exe file. You will see this window:

![gui1](https://user-images.githubusercontent.com/2302171/90901574-20527e00-e399-11ea-85dc-1b3ee7e5b7ba.png)

Note: If you get this warning from Windows:

![wd1](https://user-images.githubusercontent.com/2302171/61298234-dc5f7380-a7ab-11e9-8ff2-569aef1d51d0.png)

Just select 'More info' and then click 'Run anyway':

![wd2](https://user-images.githubusercontent.com/2302171/61299078-69ef9300-a7ad-11e9-88cd-d2b2190bc426.png)

Then, select the top folder where the files are (all folders inside this one will have their own md5 file). 
Select 'Save log to file' to save the process log into a file (recommended for troubleshooting
and production projects):

![md52](https://user-images.githubusercontent.com/2302171/61298021-82f74480-a7ab-11e9-900a-ea8cb2ef3b56.png)

Enter the extensions to ignore, separated by commas:

![md53](https://user-images.githubusercontent.com/2302171/61298034-88ed2580-a7ab-11e9-862e-ca81a1ec0780.png)

Select the format in which to write the MD5 hashes:

![md54](https://user-images.githubusercontent.com/2302171/61298050-8db1d980-a7ab-11e9-9550-3a8312ccd1aa.png)

That is it! The script will run each folder recursively and write an md5 file with this name: [folder_name]\_[date_time].md5

# License

Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
