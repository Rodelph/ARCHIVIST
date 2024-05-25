using System;

// This corresponds to the JSON data that is stored in each
// dynamic QR (which ultimately provides enough information to 
// fetch the correct hyperlink information from our database)
[System.Serializable]
public class QRData
{
    public string id;
    public int page;
}
