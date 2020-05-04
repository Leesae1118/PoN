import csv

def save_to_file(jobs):
  file = open("jobs.csv", mode="w")
  #mode는 read, write
  writer=csv.writer(file)
  writer.writerow(["title", "company", "location", "apply_link"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return 