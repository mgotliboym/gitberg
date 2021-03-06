# these methods with signature: action(repo, *args, **kwargs)
# can be applied to a repo

from .book import Book
from .make import NewFilesHandler
from .parameters import GITHUB_ORG as orgname

def get_id(repo):
    book = Book(None, repo_name=repo)

    repo = book.github_repo.github.repository(orgname, repo)
    print repo.id
    return repo.id

def get_book(repo_name):
    return Book(None, repo_name=repo_name)

def get_cloned_book(repo_name):
    book = get_book(repo_name)
    book.clone_from_github()
    book.parse_book_metadata()
    return book

def delete(repo_name):
    book = get_book(repo_name)

    repo = book.github_repo.github.repository(orgname, repo_name)
    if repo:
        if repo.delete():
            print "{} deleted".format(repo_name)
        else:
            print "couldn't delete {}".format(repo_name)
    else:
        print "{} didn't exist".format(repo_name)

def add_generated_cover(repo_name, tag=False):
    book = get_cloned_book(repo_name)

    result = book.add_covers() # None if there was already a cover
    if result:
        book.local_repo.add_all_files()
        book.local_repo.commit(result)
    return book

def config_travis(repo_name, tag=False):
    book = get_cloned_book(repo_name)

    filemaker = NewFilesHandler(book)
    filemaker.travis_files()
    book.local_repo.commit('Configure travis files')
    return book

def refresh_repo(repo_name):
    book = get_cloned_book(repo_name)
    filemaker = NewFilesHandler(book)
    filemaker.travis_files()
    book.add_covers()
    book.local_repo.add_all_files()
    book.local_repo.commit('Update cover, travis files')
    book.tag()
    return book


    