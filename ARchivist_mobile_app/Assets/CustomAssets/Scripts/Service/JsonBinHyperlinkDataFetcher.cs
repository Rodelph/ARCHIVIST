using System;
using System.Net.Http;
using System.Threading.Tasks;
using UnityEngine;
using System.Collections;

// This class can be used to fetch & serialize hyperlink information for an
// augmented document from our JsonBin.io data store. In order to find
// that information, it just needs to know which ID is associated with that
// document, and which page number the user is currently examining.
public class JsonBinHyperlinkDataFetcher
{

    private readonly HttpClient _httpClient;
    private readonly string _baseUrl = "https://api.jsonbin.io/v3/b";

    // WARNING: Storing access keys directly in source code is a VERY BAD security issue.
    // We make an exception in this case because we don't have time to more properly handle
    // this stuff, but we've tried to at least limit the permissions of this key to "read-only"
    private readonly string _accessKey = "$2a$10$yckRbDdI1n4Iq5GWwSzfS.ur6Awhp5pRwvt6BB5qROVSOLeI.oMqK";

    public JsonBinHyperlinkDataFetcher()
    {
        _httpClient = new HttpClient();
        _httpClient.DefaultRequestHeaders.Add("X-Access-Key", _accessKey);
    }

    public async void FetchJSONFromId(string id, int pageNum, Action<string, int, ARDocumentData> processHyperlinkData)
    {
        try
        {
            string url = string.Format("{0}/{1}/latest", _baseUrl, id);
            HttpResponseMessage response = await _httpClient.GetAsync(url);
            response.EnsureSuccessStatusCode(); // Throws exception for non-success status codes
            string json = await response.Content.ReadAsStringAsync();

            // Deserialize JSON string
            RecordWrapper<ARDocumentData> wrapper = JsonUtility.FromJson<RecordWrapper<ARDocumentData>>(json);

            // Access the original object
            ARDocumentData arDocumentData = wrapper.record;

            // Process the hyperlinks based on the passed in "processHyperlinkData" function
            processHyperlinkData(id, pageNum, arDocumentData);
        }
        catch (HttpRequestException e)
        {
            Console.WriteLine("Error occurred: {0}", e.Message);
        }
    }
}