class Socket_Parser():


    def __init__(self):
        from argparse import ArgumentParser as argparse_Parser
        from argparse import FileType as argparse_FileType
        from argparse import RawDescriptionHelpFormatter as Formatter

        self.INDENT = '\n  '
        INDENT = self.INDENT
        PREFIX = '@'
        DESCRIPTION = f"description:{INDENT}Python <SCRIPT> for indexation, ANSI color highlighting and redacting of text streams."
        EPILOG = f'''use cases:\
                 {INDENT}<NAME> an absolute/relative path to the corresponding file NAME\
                 {INDENT}{PREFIX}<NAME> '{PREFIX}'-prefixed call of configuraton file NAME with a newline-separated list of parse arguments
                 {INDENT}<python.exe> <SCRIPT> [options]\
                 {INDENT}<python.exe> <SCRIPT> {PREFIX}<NAME> [options]\
                 '''
        parser = argparse_Parser( description           = DESCRIPTION,
                                  epilog                = EPILOG,
                                  fromfile_prefix_chars = PREFIX,
                                  formatter_class       = Formatter )
        parser.add_argument("--host_SERVER", help="server address host : '127.0.0.1', 'localhost', ... ")
        parser.add_argument("--port_SERVER", help="server address port : 0, 1024-65535", type=int)
        parser.add_argument("--host_CLIENT", help="client address host : '127.0.0.1', 'localhost', ... ")
        parser.add_argument("--port_CLIENT", help="client address port : 0, 1024-65535", type=int)
        parser.add_argument("--timeout",     help="socket TIMEOUT : 0,1,2-...(sec)",type=int)
        parser.add_argument("--backlog",     help="maximum number of connected clients",type=int)
        parser.add_argument("--verbosity",   help="VERBOSITY of output: 0.Silent  1.Verbose",type=int)
        parser.add_argument("--message",     help="a MESSAGE to copy via the sever and client sockets")
        parser.add_argument("--repeat",      help="number of repetitions of the MESSAGE",type=int)
        parser.set_defaults( host_SERVER = '127.0.0.1',
                             port_SERVER = 44444,
                             host_CLIENT = 'localhost',
                             port_CLIENT = 44445,
                             timeout     = 10,
                             backlog     = 1,
                             verbosity   = 1,
                             repeat      = 1,
                             message     = "A message from Python socket." )
        self.parser = parser
# ....... End of __init__() .......




    def parse(self):
        args,other = self.parser.parse_known_args()
        if args.verbosity>=1:
            print(f"\nParsed Arguments:{self.INDENT}{args}{self.INDENT}{other}")
        return vars(args)
# ....... End of parse() .......




    def help(self):
        self.parser.print_help()
# ....... End of help() .......
# ....... End of Parser .......




if __name__=='__main__':
    from sys import argv
    if len(argv)>1: Socket_Parser().parse()
    else:           Socket_Parser().help()


