# photo-repo
## Winter 2022 - Shopify Developer Intern Challenge Question
Pratham Thukral

# Stack used:
* Django (Python 3.8.8 + Django 3.2.7)
* AWS RDS MySQL DB for Image meta data storage + management
* AWS S3 Buckets for Image storage

# Installation Guide
1. Clone repository
2. Navigate in console to `ShopifyBackendChallenge_W22/ShopifyProject/`
3. Add in S3 and RDS Keys from AWS account into `ShopifyProject\ShopifyProject\settings.py`. 
    - These have been blocked out from this repository submission for security reasons
5. Run `python.exe .\manage.py runserver`

# Testing

## Adding Image to Repo (POST Request)
1. Upload image to `ShopifyProject/media` folder
    - Ensure the filename is unique as this is used as a key for deletion + searching
    - `cat.png` and `dog.jpg` are provided for testing
2. Navigate to `127.0.0.1:8000/image`
3. Generate a POST request with the request body:
```json
{
    "filename": "<< filename >>",
    "tag": "<< optional tag; leave blank for null >>"
}
```
3. A successful POST request will return success JSON, insert into SQL, and insert into S3 bucket
4. ![postman POST Request](/ShopifyProject/testing_screenshots/postman_POST_req.PNG?raw=true)
5. ![sql POST Request](/ShopifyProject/testing_screenshots/sql_POST_req.PNG?raw=true)
6. ![s3 POST Request](/ShopifyProject/testing_screenshots/s3_POST_req.PNG?raw=true)


## Searching for Images
### Return all images
1. Navigate to `127.0.0.1:8000/image`
2. Generate a GET request with no query parameters (the same url listed in step 1)
3. This will `SELECT * FROM << image database >>`
4. ![postman GET Request](/ShopifyProject/testing_screenshots/postman_GET_req_no_filter.PNG?raw=true)

### Searching for Images using Filename (GET Request)
1. Navigate to `127.0.0.1:8000/image?filename=<< filename >>`
2. If there is a filename that matches exactly, it will be returned
4. ![postman GET Request](/ShopifyProject/testing_screenshots/postman_GET_req_filename_filter.PNG?raw=true)
5. Else there will be a JSON response saying no results found
6. ![postman GET Request](/ShopifyProject/testing_screenshots/postman_GET_req_filename_filter_fail.PNG?raw=true)

### Searching for Images using Tag (GET Request)
1. Navigate to `127.0.0.1:8000/image?tag=<< tag >>`
2. This queries all images with `Tag LIKE '%<< tag >>%'`
    - This is so multiple tags can be stored per image, regardless of delimiter/format 
4. Results returned if found
5. ![postman GET Request](/ShopifyProject/testing_screenshots/postman_GET_req_tag_filter.PNG?raw=true)

### Deleting Image from Repo (DELETE Request)
2. Navigate to `127.0.0.1:8000/image`
3. Generate a DELETE request with the request body:
```json
{
    "filename": "<< filename >>",
}
```
3. Example of a successful DELETE request:
4. ![postman Delete Request](/ShopifyProject/testing_screenshots/postman_DELETE_req.PNG?raw=true)
5. This will remove the file meta data from SQL and remove the object from the s3 bucket

# Next Steps
- There's no frontend developed for these API calls, so actions like uploading images is manual
- There's also no functionality for bulk adding/deleting files based of tag or filenames
- Some sort of user authentication, so user can only view their own images + public ones
    - this could lead to buy/sell marketplace idea listed in the challenge document
- Another interesting idea would be to incorporate computer vision to attempt to auto-tag images

