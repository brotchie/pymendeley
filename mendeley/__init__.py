"""
Access document data in the Mendeley sqlite3 database.

 - Currently looks in fixed paths on Linux. Changing
   EXPECTED_MENDELEY_SQLITE_DIR and EXPECTED_MENDELEY_CONFIG_PATH
   should allow it to work on non-linux or non-standard
   installs.

"""
import os
import sqlite3
from ConfigParser import ConfigParser

# On Linux we can usually find the Mendeley sqlite3 database
# at this location.
EXPECTED_MENDELEY_SQLITE_DIR = os.path.expanduser('~/.local/share/data/Mendeley Ltd./Mendeley Desktop')
EXPECTED_MENDELEY_CONFIG_PATH = os.path.expanduser('~/.config/Mendeley Ltd./Mendeley Desktop.conf')

def find_mendeley_sqlite_path():
    """
    Returns the path to the Mendeley sqlite3 database if in
    standard location, otherwise returns None.

    """
    try:
        if os.path.exists(EXPECTED_MENDELEY_CONFIG_PATH):
            cp = ConfigParser()
            cp.read(EXPECTED_MENDELEY_CONFIG_PATH)

            email = cp.get('MendeleyWeb', 'userEmail')

            candidate_path = os.path.join(EXPECTED_MENDELEY_SQLITE_DIR, '%s@www.mendeley.com.sqlite' % (email,))
            if os.path.exists(candidate_path):
                return candidate_path
    except StandardError:
        pass

    return None

class MendeleyDatabaseInterface(object):
    def __init__(self, path=None):
        self.path = path or find_mendeley_sqlite_path()

    def get_references(self):
        """
        Retrieves all references from the Mendeley database
        and returns a list of MendeleyReferences.

        """
        with sqlite3.connect(self.path) as db:
            c = db.execute("SELECT Documents.uuid, group_concat(DocumentContributors.lastName, ', ') as authors, Documents.year, Documents.title , Documents.publication FROM DocumentContributors, Documents WHERE Documents.id=DocumentContributors.documentId group by Documents.year, Documents.title ORDER BY authors;")
            return [MendeleyReference(*row) for row in c]

    def get_reference_by_citation_key(self, citekey):
        with sqlite3.connect(self.path) as db:
            c = db.execute("SELECT Documents.uuid, group_concat(DocumentContributors.lastName, ', ') as authors, Documents.year, Documents.title , Documents.publication FROM DocumentContributors, Documents WHERE Documents.id=DocumentContributors.documentId AND Documents.citationKey=? GROUP BY Documents.year, Documents.title ORDER BY authors;", (citekey,))
            row = c.fetchone()
            if row:
                return MendeleyReference(*row)
            else:
                return None

    def get_reference_path_by_uuid(self, uuid):
        """
        For a given document UUID, looks up and returns
        its first local file url.

        """
        with sqlite3.connect(self.path) as db:
            c = db.execute("SELECT Files.localUrl FROM Files, DocumentFiles, Documents WHERE Files.hash = DocumentFiles.hash AND DocumentFiles.documentId = Documents.id AND Documents.uuid=? LIMIT 1", (uuid,))
            row = c.fetchone()
            if row:
                localurl, = row
                return localurl
            else:
                return None

class MendeleyReference(object):
    """
    Simple class to hold a Mendeley document's reference
    data.

    """
    def __init__(self, uuid, authors, year, title, publication):
        self.uuid = uuid
        self.authors = authors
        self.year = year
        self.title = title
        self.publication = publication

    def as_text_reference(self):
        if self.year:
            return '%s - %d - %s' % (self.authors, self.year, self.title)
        else:
            return '%s - %s' % (self.authors, self.title)

    def __repr__(self):
        return 'MendeleyReference(%s)' % (', '.join(repr(x) for x in [self.uuid, self.authors, self.year, self.title, self.publication]))
