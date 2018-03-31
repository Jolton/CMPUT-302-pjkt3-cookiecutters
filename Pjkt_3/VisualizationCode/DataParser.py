import csv
import DataStructures
import datetime


def findLibraryInListOfDomains(domains, libraryName):
    for domain in domains:
        library = domain.containsLibraryWithName(libraryName)
        if library is not None:
            return library

    return None


def parseTables():

    domains = []
    k = 0
    # read the Library info data and make domains and add the libraries to them
    with open('TableData/Metric Data - Library Info.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for (libraryName, gitHubRepo, domainName) in reader:
            domain = DataStructures.Domain.arrayContainsWithName(domains, domainName)
            if domain is None:
                domain = DataStructures.Domain(domainName)
                domains.append(domain)

            library = domain.containsLibraryWithName(libraryName)
            if library is None:
                library = DataStructures.Library(libraryName)
                domain.addLibrary(library)

            library.gitHubRepository = gitHubRepo


    # add popularity data
    with open('TableData/Metric Data - Popularity.csv') as csvfile:
        # start reading the file
        reader = csv.reader(csvfile)
        next(reader) # skips the first line of the file because its the header
        # for each line of data in the file
        for (libraryName, popularityCount) in reader:
            # find the library with that matches this line in the file
            library = findLibraryInListOfDomains(domains, libraryName)
            # if the library wasn't found then skip this line
            if library is None:
                print("----------ERROR IN Popularity Data----------")
                print('library: /"' + libraryName + '/" not initialised')
                continue
            library.popularity = popularityCount


    # add Release data
    with open('TableData/Metric Data - Release Frequency.csv') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        data = []
        for array in reader:
            data.append(array)

        for domain in domains:
            i = -1
            for library in domain.libraries:
                for idx, val in enumerate(header):
                    if library.name in val:
                        i = idx
                for line in data:
                    if line[i] == '':
                        break
                    dateStrs = line[i].split("-")
                    library.releaseDates.append(datetime.date(int(dateStrs[0]), int(dateStrs[1]), int(dateStrs[2])))

                library.releaseDates.sort()

    # adds last mod data
    with open('TableData/Metric Data - Last Modification Date.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for (libraryName, lastModDate) in reader:
            library = findLibraryInListOfDomains(domains, libraryName)

            if library is None:
                print("----------ERROR IN Last Mod Date----------")
                print('library: /"' + libraryName + '/" not initialised')
                continue
            dateStrs = lastModDate.split("-")
            library.lastModificationDate = datetime.date(int(dateStrs[0]), int(dateStrs[1]), int(dateStrs[2]))

    # adds backwards compatibility data
    with open('TableData/Metric Data - Backwards Compatibility.csv') as csvfile:
        reader = csv.reader(csvfile)

        header = next(reader)

        data = []
        for line in reader:
            data.append(line)

        for domain in domains:
            i = -1
            for library in domain.libraries:
                for idx, val in enumerate(header):
                    if library.name in val:
                        i = idx
                        break

                for line in data:
                    if line[i] == '':
                        break
                    library.breakingChangesPerRelease.append((line[0], int(line[i])))



    # adds stackoverflow data
    with open('TableData/Metric Data - Last Discussed on Stack Overflow.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for (libraryName, lastDiscussed, numOfQuestions) in reader:
            library = findLibraryInListOfDomains(domains, libraryName)
            if library is None:
                print("----------ERROR IN Discussed on stack overflow----------")
                print('library: /"' + libraryName + '/" not initialised')
                continue


            if lastDiscussed == 'Never':
                library.lastDiscussedOnStackOverflow = lastDiscussed
            else:
                dateStrs = lastDiscussed.split("-")
                library.lastDiscussedOnStackOverflow = datetime.date(int(dateStrs[0]), int(dateStrs[1]), int(dateStrs[2]))

            library.questionsAsked = numOfQuestions



    # adds issue data
    with open('TableData/Metric Data - Issue Data.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for (issueId, libraryName, issueCreationDate, issueClosingDate, firstComment, performance, security) in reader:
            library = findLibraryInListOfDomains(domains, libraryName)
            if library is None:
                print("----------ERROR IN issue data----------")
                print('library: /"' + libraryName + '/" not initialised')
                continue

            issue = DataStructures.Issue()
            issue.id = issueId

            if issueCreationDate != 'None':
                dateStrs = issueCreationDate.replace(' ', '-').replace(':', '-').split("-")
                issue.creationDate = datetime.datetime(int(dateStrs[0]), int(dateStrs[1]), int(dateStrs[2]), int(dateStrs[3]), int(dateStrs[4]), int(dateStrs[5]))
                # issue.creationDate = datetime.datetime.strptime(issueCreationDate, "%Y-%m-%d %H:%M:%S")

            if issueClosingDate != 'None':
                dateStrs = issueClosingDate.replace(' ', '-').replace(':', '-').split("-")
                issue.closingDate = datetime.datetime(int(dateStrs[0]), int(dateStrs[1]), int(dateStrs[2]),
                                                       int(dateStrs[3]), int(dateStrs[4]), int(dateStrs[5]))

            if firstComment != 'None':
                dateStrs = firstComment.replace(' ', '-').replace(':', '-').split("-")
                issue.firstCommentDate = datetime.datetime(int(dateStrs[0]), int(dateStrs[1]), int(dateStrs[2]),
                                                       int(dateStrs[3]), int(dateStrs[4]), int(dateStrs[5]))

            issue.performance = performance == 'Yes'
            issue.security = security == 'Yes'

            library.issues.append(issue)


    return domains























