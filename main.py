import os
import google.auth
import google.auth.transport.requests
import google.oauth2.credentials
import googleapiclient.discovery
import googleapiclient.errors

def search_comments(youtube, video_id, search_term):
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100
        )
        while request:
            response = request.execute()
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                if search_term in comment:
                    print(f"\033[94m{author}\033[0m: {comment}")
            request = youtube.commentThreads().list_next(request, response)
    except googleapiclient.errors.HttpError as e:
        if e.resp.status == 403 and "disabled comments" in e.content.decode().lower():
            print("This video has comments turned off.")
        else:
            raise e

def main():
    # Get user input for the YouTube video ID and search term
    video_id = input("Enter the YouTube video ID: ")
    search_term = input("Enter the word or phrase to search for in the comments: ")

    # Set up the YouTube Data API client
    api_service_name = "youtube"
    api_version = "v3"
    key_file_location = "/home/cam/Youtube Skimmer/authentication.json"
    credentials = google.oauth2.service_account.Credentials.from_service_account_file(key_file_location, scopes=["https://www.googleapis.com/auth/youtube.force-ssl"])

    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    # Call the search_comments function to retrieve and search the comments
    search_comments(youtube, video_id, search_term)

if __name__ == "__main__":
    main()

# def search_comments(youtube, video_id, search_term, max_results):
#     results = []
#     request = youtube.commentThreads().list(
#         part="snippet",
#         videoId=video_id,
#         textFormat="plainText",
#         maxResults=100
#     )
#     while request and len(results) < max_results:
#         response = request.execute()
#         for item in response["items"]:
#             comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
#             author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
#             if search_term in comment:
#                 results.append((author, comment))
#         request = youtube.commentThreads().list_next(request, response)
#         if "nextPageToken" in response:
#             request = youtube.commentThreads().list(
#                 part="snippet",
#                 videoId=video_id,
#                 textFormat="plainText",
#                 maxResults=100,
#                 pageToken=response["nextPageToken"]
#             )
#     return results

# def main():
#     # Get user input for the YouTube video ID and search term
#     video_id = input("Enter the YouTube video ID: ")
#     search_term = input("Enter the word or phrase to search for in the comments: ")
#     max_results = int(input("Enter the maximum number of results to retrieve: "))

#     # Set up the YouTube Data API client
#     api_service_name = "youtube"
#     api_version = "v3"
#     key_file_location = "/home/cam/Youtube Skimmer/authentication.json"
#     credentials = google.oauth2.service_account.Credentials.from_service_account_file(key_file_location, scopes=["https://www.googleapis.com/auth/youtube.force-ssl"])

#     youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

#     # Call the search_comments function to retrieve and search the comments
#     comments = search_comments(youtube, video_id, search_term, max_results)
#     if comments:
#         for author, comment in comments:
#             print(f"{author}: {comment}")
#     else:
#         print("No comments found.")
# if __name__ == "__main__":
#     main()

