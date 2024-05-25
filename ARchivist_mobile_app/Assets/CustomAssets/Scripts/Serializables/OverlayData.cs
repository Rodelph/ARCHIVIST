using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// This class is used to temporarily store information about each
// hyperlink overlay that needs to be spawned (after we've fetched
// hyperlink data for a document from our database).
public class OverlayData
{

    // originalWebsiteUrl is technically optional, since if we tell our computer app to use
    // a local HTML file to generate an augmented document, then we have no URL
    // associated with the augmented document
#nullable enable
    public string? originalWebsiteUrl;
#nullable disable
    public string hyperlinkUrl;
    public Vector3 scale;
    public Vector3 offset;

    public OverlayData(string originalWebsiteUrl, string hyperlinkUrl, Vector3 scale, Vector3 offset)
    {
        this.originalWebsiteUrl = originalWebsiteUrl;
        this.hyperlinkUrl = hyperlinkUrl;
        this.scale = scale;
        this.offset = offset;
    }
}
