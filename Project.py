import urllib2

EXTENSIONS_TO_ANALYZE = [".c", ".cpp", ".h", ".hpp"]
CURLY_TRIGGERS = ["if", "while", "for", "switch"]
CURLY_SAME = 0
CURLY_NEXT = 1
CURLY_OTHER = 2

class Project:
    def __init__(self, github_project):
        self.github_project = github_project
        self.init_stats()
    
    def init_stats(self):
        self.curly_same = 0
        self.curly_next = 0
        self.curly_other = 0
    
    
    def get_files(self):
        results = []
        for a_file in self.github_project.get_branch("master").commit.files:
            for extension in EXTENSIONS_TO_ANALYZE:
                if a_file.filename.endswith(extension):
                    results.append(a_file)
                    break
        
        return results
        
    def get_file_contents(self, a_file):
        return urllib2.urlopen(a_file.raw_url).read()
    
    def get_curly_style(self, line1, line2):
        if line1[-1] == "{":
            return CURLY_SAME
        elif len(line2) == 1 and line2[0] == "{":
            return CURLY_NEXT
        else:
            return CURLY_OTHER
    
    def analyze_c_file(self, contents):
        lines = contents.split("\n")
        for i in range(len(lines)):
            line = lines[i].strip()
            for trigger in CURLY_TRIGGERS:
                if line.startswith(trigger):
                    style = self.get_curly_style(line, lines[i + 1].strip())
                    if style == CURLY_SAME:
                        self.curly_same += 1
                    elif style == CURLY_NEXT:
                        self.curly_next += 1
                    else:
                        self.curly_other += 1
                    break