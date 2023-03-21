# # import uuid
# # from flask import Flask, request, jsonify
# # import requests
# # from bs4 import BeautifulSoup

# # app = Flask(__name__)


# # @app.route('/freelancer', methods=['GET'])
# # def scrape_freelancer():
# #     base_url = "https://www.freelancer.com"
# #     url = "https://www.freelancer.com/jobs"
# #     query_params = request.args.to_dict()

# #     # Set up the request parameters

# #     params = {
# #         "keywords": query_params.get('keywords'),
# #         "limit": query_params.get('limit', '50'),
# #         "offset": query_params.get('offset', '0'),
# #         "job_status": query_params.get('job_status'),
# #         "project_type": query_params.get('project_type'),
# #         "budget_range": query_params.get('budget_range'),
# #         "sort": query_params.get('sort', 'latest'),
# #         "languages[]": query_params.get('languages[]'),
# #         "skills[]": query_params.get('skills[]'),
# #         "job_success": query_params.get('job_success')
# #     }

# #     # Send the request to the server and get the response
# #     response = requests.get(url, params=params)
# #     soup = BeautifulSoup(response.content, 'html.parser')

# #     # Extract the job cards and get information about each job
# #     jobs = []
# #     job_cards = soup.find_all('div', class_='JobSearchCard-item-inner')
# #     print(len(job_cards))
# #     for card in job_cards:
# #         job = {}

# #         # Generate a random ID for each job
# #         job['job_id'] = str(uuid.uuid4())

# #         job_title = card.find('a', class_='JobSearchCard-primary-heading-link')
# #         job['title'] = job_title.text.strip() if job_title else None

# #         job['status'] = 'open'

# #         job_link = card.find(
# #             'a', class_='JobSearchCard-primary-heading-link')['href']
# #         job['link'] = base_url + job_link if job_link else None

# #         job_desc = card.find('p', class_='JobSearchCard-primary-description')
# #         job['description'] = job_desc.text.strip() if job_desc else None

# #         # job_budget = card.find('span', class_='JobSearchCard-primary-price')
# #         # job['budget'] = job_budget.text.strip() if job_budget else None

# #         job_skills = card.find_all(
# #             'a', class_='JobSearchCard-primary-tagsLink')
# #         job['skills'] = [skill.text.strip()
# #                          for skill in job_skills] if job_skills else None

# #         job_bids = card.find('div', class_='JobSearchCard-secondary-price')
# #         job['bids'] = job_bids.text.strip() if job_bids else None

# #         job_proposals = card.find(
# #             'div', class_='JobSearchCard-secondary-entry')
# #         job['proposals'] = job_proposals.text.strip() if job_proposals else None

# #         job_verified = card.find(
# #             'div', class_='JobSearchCard-primary-heading-status Tooltip--top')
# #         job['verified'] = True if job_verified else False

# #         job_time = card.find(
# #             'span', class_='JobSearchCard-primary-heading-days')
# #         job['time'] = job_time.text.strip() if job_time else None

# #         jobs.append(job)

# #     return jsonify(jobs)


# # if __name__ == '__main__':
# #     app.run(debug=True)


# # from flask import Flask, jsonify
# # import requests
# # from bs4 import BeautifulSoup

# # app = Flask(__name__)


# # @app.route('/jobs')
# # def get_jobs():
# #     # Set the headers to avoid 403 Forbidden error
# #     headers = {
# #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
# #     }

# #     # # Set up a proxy server
# #     # proxy_url = 'http://your-proxy-url.com'
# #     # proxies = {
# #     #     'http': proxy_url,
# #     #     'https': proxy_url
# #     # }

# #     # Send an HTTP request to the Upwork job search page using the proxy server
# #     url = 'https://www.upwork.com/jobs/search/'
# #     response = requests.get(url, headers=headers)

# #     # Check for errors
# #     if response.status_code != 200:
# #         return 'Error: Unable to access Upwork site'

# #     # Parse the HTML content of the response
# #     soup = BeautifulSoup(response.text, 'html.parser')

# #     # Locate the relevant HTML elements that contain job data
# #     job_titles = soup.find_all('a', {'class': 'job-title-link'})
# #     job_descriptions = soup.find_all('div', {'class': 'job-description'})

# #     # Extract the job data from the HTML elements
# #     jobs = []
# #     for i in range(len(job_titles)):
# #         title = job_titles[i].get_text().strip()
# #         description = job_descriptions[i].get_text().strip()

# #         # Append the job data to the jobs list
# #         jobs.append({'title': title, 'description': description})

# #     # Return the jobs list as JSON data
# #     return jsonify(jobs)


# # if __name__ == '__main__':
# #     app.run(debug=True, port=5000)


# from flask import Flask, jsonify
# import requests
# from bs4 import BeautifulSoup

# app = Flask(__name__)


# @app.route('/')
# def get_job_data():
#     url = 'https://ureed.com/find-projects'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     job_items = soup.find_all('div', class_='mb-8 sm:px-5 px-2')

#     jobs = []
#     for job_item in job_items:
#         title_element = job_item.find(
#             'h4', class_='text-lg font-semibold mb-2')
#         title = title_element.text.strip()
#         description_element = job_item.find(
#             'p', class_='text-gray-500 text-sm mb-2')
#         description = description_element.text.strip()
#         category_element = job_item.find(
#             'div', class_='text-xs text-gray-400 mb-1', text='Category:')
#         category = category_element.find_next('div').text.strip()
#         budget_element = job_item.find(
#             'div', class_='text-xs text-gray-400 mb-1', text='Budget:')
#         budget = budget_element.find_next('div').text.strip()
#         duration_element = job_item.find(
#             'div', class_='text-xs text-gray-400 mb-1', text='Duration:')
#         duration = duration_element.find_next('div').text.strip()
#         proposals_element = job_item.find(
#             'div', class_='text-xs text-gray-400 mb-1', text='Proposals:')
#         proposals = proposals_element.find_next('div').text.strip()

#         job = {
#             'title': title,
#             'description': description,
#             'category': category,
#             'budget': budget,
#             'duration': duration,
#             'proposals': proposals
#         }

#         jobs.append(job)

#     return jsonify(jobs)


# if __name__ == '__main__':
#     app.run(debug=True)
