# ARchivist

<h2> This game was made by :  </h2>
<table style="width:100%" align="center">
    <tr>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Student ID</th>
    </tr>
    <tr>
        <td>Amine</td>
        <td>Naqi</td>
        <td>0562497</td>
    </tr>    
    <tr>
        <td>Mable</td>
        <td>Rajan</td>
        <td></td>
    </tr>
    <tr>
        <td>Sean Victor</td>
        <td>Scofield</td>
        <td></td>
    </tr>    
</table>

## Overview

This project contains the code for the ARchivist prototype built for
the Next Generation User Interfaces course at VUB. It was written by
Amine Naqi, Mable Rajan, and Sean Scofield.

ARchivist is a project that is meant to make hyperlinks visible and interactive on physical documents. In its current state, it can be used to create an "augmented" document from a website page (which generates a PDF of that website page containing a QR code and AR marker on each page). By scanning those QR codes, users of the ARchivist mobile application can them view and interact with a document's hyperlinks via augmented reality.

The code in this repo is separate into 2 sub-parts, each containing their own respective sub-directories and README files:
- **ARchivist document generator**: Python code to be run on a computer in order to generate augmented documents
- **ARchivist mobile application**: Unity project containing the code for an Android/iPhone mobile application that can be used to read and interact with these augmented documents.

In addition, a pre-built Android APK of the mobile application has been included for ease of testing this prototype. Note, however, that the AR tracking performance is noticeably better on iPhone. For both Android and iPhone, the Unity project can be opened and used to package the application into an Android or iPhone app (the latter requiring MacOS).

## Compatibility

This project is meant to be compatible with the following operating systems (although macOS is required for building an iPhone app from the mobile application):

- **Windows**
- **Linux**
- **macOS**
