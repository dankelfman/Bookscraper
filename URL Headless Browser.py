import requests
import csv
import concurrent.futures

def format_url(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        return 'https://' + url
    return url

def get_status_code(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    formatted_url = format_url(url)
    try:
        response = requests.get(formatted_url, headers=headers, timeout=30, allow_redirects=True)
        return response.status_code, status_code_explanations.get(response.status_code, 'Unknown status code')
    except requests.exceptions.RequestException:
        return 'Error', status_code_explanations['Error']

status_code_explanations = {
    200: 'OK - The request has succeeded',
    301: 'Moved Permanently - The URL of the requested resource has been changed permanently',
    302: 'Found - The URL of the requested resource has been changed temporarily',
    400: 'Bad Request - The server could not understand the request due to invalid syntax',
    401: 'Unauthorized - Authentication is needed to get requested response',
    403: 'Forbidden - Client does not have access rights to the content',
    404: 'Not Found - The server can not find the requested resource',
    500: 'Internal Server Error - The server has encountered a situation it does not know how to handle',
    502: 'Bad Gateway - The server, while acting as a gateway or proxy, received an invalid response',
    503: 'Service Unavailable - The server is not ready to handle the request',
    'Error': 'Could not process the request (timeout, invalid, etc.)'
}

def write_to_csv(file_name, data):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Company Domain Name', 'Status Code', 'Explanation'])
        for item in data:
            writer.writerow(item)

with open('D:\\Coding\\url_status80k.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    urls = [format_url(row['Company Domain Name']) for row in reader if row['Company Domain Name']]

# Start processing from the 30,001st URL
start_from_url = 30000
urls = urls[start_from_url:]

count, total_urls = 0, len(urls)
print(f"Total URLs to process: {total_urls}")

results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    future_to_url = {executor.submit(get_status_code, url): url for url in urls}
    for future in concurrent.futures.as_completed(future_to_url):
        count += 1
        url = future_to_url[future]
        try:
            status, explanation = future.result()
        except Exception as exc:
            results.append([url, 'Error', 'Exception occurred: ' + str(exc)])
        else:
            results.append([url, status, explanation])

        if count % 250 == 0:
            print(f"Processed {count}/{total_urls} URLs...")

        # Adjust the output file index based on the starting point
        file_index = (start_from_url + count) // 10000
        if count % 10000 == 0 or count == total_urls:
            output_file = f'D:\\Coding\\url_status_{file_index}.csv'
            write_to_csv(output_file, results)
            results = []  # Reset for next batch

print("Processing complete.")
