using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

// This class can be used to fetch & serialize hyperlink information for an
// augmented document from the github repo being used for centralized storage. 
// In order to find that information, it just needs to know which ID is associated 
// with that, document, and which page number the user is currently examining.

// NOTE THAT THIS IS CURRENTLY NOT BEING USED (JsonBin.io is being used instead), 
// but is here in case anyone would like to develop this piece out further.
public class GithubHyperlinkDataFetcher
{
    // URL in our github repo where we are storing the JSON files containing
    // the hyperlink information for each augmented document
    private string url = "https://raw.githubusercontent.com/seanscofield/archivist/main/Assets/CustomAssets";

    public IEnumerator FetchJSONFromId(string id, int pageNum, Action<string, int, ARDocumentData> processHyperlinkData)
    {
        string fullUrl = $"{url}/{id}.json";

        using (UnityWebRequest www = UnityWebRequest.Get(fullUrl))
        {
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError($"Error fetching JSON from URL: {www.error}");
            }
            else {
                ARDocumentData arDocumentData = JsonUtility.FromJson<ARDocumentData>(www.downloadHandler.text);
                processHyperlinkData(id, pageNum, arDocumentData);
            }
        }
    }
}
