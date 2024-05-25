using System;
using System.Collections.Generic;

// Define classes to represent and serialize the JSON structure that
// we're using in our database to store all of the hyperlink information
// for an augmented document
[System.Serializable]
public class ARDocumentData
{
    public float[] ar_marker_coordinates;
    public List<Page> pages;

    // URL is technically optional, since if we tell our computer app to use
    // a local HTML file to generate an augmented document, then we have no URL
    // associated with the augmented document
#nullable enable
    public string? URL;
#nullable disable
}

[System.Serializable]
public class Page
{
    public List<Hyperlink> hyperlinks;
}

[System.Serializable]
public class Hyperlink
{
    public string uri;
    public float[] coordinates;
}

// Define a wrapper class to handle optional "record" item
[System.Serializable]
public class RecordWrapper<T>
{
    public T record;
}
