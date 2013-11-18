#number of projects per language
bq query 'SELECT repository_language, count(repository_language) as pushes
FROM [githubarchive:github.timeline]
WHERE type="CreateEvent" and repository_fork == "false"
GROUP BY repository_language
ORDER BY pushes DESC'

#watches for a specific language 
bq query 'SELECT repository_name, count(repository_name) as watches, repository_description, repository_url
FROM [githubarchive:github.timeline]
WHERE type="WatchEvent"
    AND repository_language="Haskell"
GROUP BY repository_name, repository_description, repository_url
ORDER BY watches DESC
LIMIT 50
'
