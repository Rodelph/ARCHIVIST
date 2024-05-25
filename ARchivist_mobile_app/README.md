# ARchivist Unity Project (for mobile app)

## Overview

This directory contains the Unity project for the ARchivist Android/IOS application. Many of the files in this project existed before we started writing any application code (for example, pre-packaged assets/scripts/etc.). The only new assets that we've created can all be found under `Assets/CustomAssets`.


Here is a brief description of the sub-directories in `Assets/CustomAssets`:
- **Images** (contains the "Legend" image file that we display in AR to show what the different link colors mean)
- **Materials** (contains different colored, semi-transparent materials that we use for our prefabs)
- **Prefabs** (contains the prefabs corresponding to AR hyperlink overlays that are app places on top of the hyperlinks in augmented documents)
- **Scenes** (contains the "Hyperlinks" scene)
- **Scripts** (all of our C# scripts)

Furthermore, here is a brief description of *some* of the important C# scripts
- `QRCodeDetector.cs` C# script for continually monitoring for QR codes, and publishing a notification to other listening scripts whenever it successfully scans a code)
- `SpawnHyperlinks.cs` C# script for spawning hyperlinks whenever a QR code and AR marker are detected)
- `TapListener.cs` C# script for listening for whenever a user taps on a hyperlink overlay game object, and opening a browser page whenever that happens to follow the hyperlink)
- `util/CoordinateConverter.cs` C# script for converting between PyMuPDF coordinates and Unity AR coordinates)
- `Serializables/` folder containing C# scripts for serializing JSON objects (e.g. JSON object containing hyperlink information for a given document, fetched from our data store).
- `Service/` folder containing C# scripts for fetching data from our data stores. We're only using the JsonBin.io data store at the moment, but there is some half-fledged support for Github that could be expanded upon if one so desires.

Furthermore, note that the scripts for monitoring for QR codes & AR markers, as well as spawning hyperlinks, are attached as components to the "AR Session Origin" object in the "Hyperlinks" scene. The script for *listening* for when a user taps on a hyperlink overlay is attached to the "AR Camera" object.

## Setup Instructions
When you open the project for the first time, you will likely want to open the "Hyperlinks" scene, which can be found at `Assets/CustomAssets/Scenes/Hyperlinks`. This will allow you to see the game objects (and scripts attached to those objects) that are being used when the application runs. Currently, only the "AR Session Origin" and "AR Camera" objects have scripts attached to them.

### Building the application
In order to package this application into an Android or iPhone application, you'll need to navigate to "File -> Build Setting", and then select the `Platform` you would like to use. Note that you will only be able to build to Android and iOS if you have installed support for those platforms via Unity Hub (Note: iOS is only supported when using Unity on a Mac).

After that, you should be able to click "Build and Run" from the same "Build Settings" window in order to build the application. When using Android, this should create an APK file, but when using iOS, this will cause an Xcode project to be created (you might need an Apple Developer account).

Note that the app performs MUCH BETTER on iPhone than Android (in terms of AR tracking).

## Troubleshooting:
- To scan a qr code, make sure to get the camera close to the code while keeping it in focus.
- The AR tracking currently works much better with iPhone than with Android.
- Regardless of whether you are using iPhone or Android, you really have to keep the camera relatively close to the AR marker and refrain from jerky movements.