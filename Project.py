import urllib2

EXTENSIONS_TO_ANALYZE = [".c", ".cpp", ".h", ".hpp"]
CURLY_TRIGGERS = ["if", "while", "for", "switch"]

class Project:
    def __init__(self, github_project):
        self.github_project = github_project
        self.init_stats()
    
    def init_stats(self):
        self.curly_same = 0
        self.curly_next = 0
        self.curly_other = 0
        self.paren_prec_space = 0
        self.paren_no_prec_space = 0
        self.whitespace_spaces = 0
        self.whitespace_tabs = 0
        self.nzero_line_count = 0
        self.nzero_line_sum = 0
    
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
    
    def record_curly_style(self, line1, line2):
        if line1[-1] == "{":
            self.curly_same += 1
        elif len(line2) == 1 and line2[0] == "{":
            self.curl_next += 1
        else:
            self.curly_other += 1
        
    def record_paren_style(self, line):
        for i in range(1, len(line)):
            if line[i] == "(":
                if line[i - 1] == " ":
                    self.paren_prec_space += 1
                else:
                    self.paren_no_prec_space += 1
    
    def record_whitespace_style(self, line):
        if len(line) > 0:
            if line[0] == " ":
                self.whitespace_spaces += 1
            elif line[0] == "\t":
                self.whitespace_tabs += 1
    
    def record_nzero_line_length(self, line):
        if len(line) > 0:
            self.nzero_line_count += 1
            self.nzero_line_sum += len(line)
    
    def analyze_c_file(self, contents):
        lines = contents.split("\n")
        for i in range(len(lines)):
            line = lines[i]
            for trigger in CURLY_TRIGGERS:
                if line.strip().startswith(trigger):
                    self.record_curly_style(line.strip(), lines[i + 1].strip())
                    break
            self.record_paren_style(line.strip())
            self.record_whitespace_style(line)
            self.record_nzero_line_length(line.strip())