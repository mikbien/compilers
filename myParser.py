class MyParser:

    ##### Parser header #####
    def __init__(self, scanner, debug):
        self.debug = debug
        print('**** PARSER ****\n\n')
        self.next_token = scanner.next_token
        self.token = self.next_token()

    def take_token(self, token_type):
        if self.token.type != token_type:
            self.error(f"Expected token: {token_type}")
        if token_type != 'END':
            if self.debug is True:
                print(f"Taking {self.token}")
            self.token = self.next_token()

    def error(self,msg):
        raise RuntimeError(f"{msg} current {self.token}")

    ##### Parser body #####

    # Starting symbol
    def start(self):
        # program
        self.program()

    def program(self):
        while self.token.type != 'BEGIN':
            self.token = self.next_token()
        # program -> new_lines BEGIN NEWLINE declarations NEWLINE links END new_lines
        if self.token.type == 'BEGIN':
            print('program start')
            self.take_token('BEGIN')
            self.take_token('NEWLINE')
            print('  declarations start')
            self.declarations()
            print('  declarations ok')
            self.module_separator()
            print('  links start')
            self.links()
            print('  links ok')
            self.take_token('END')
            print('program ok')
        else:
            self.error('Expected BEGIN token')
            
    
    def declarations(self):
        # declarations -> declaration declarations        
        if self.token.type == 'ID':
            self.declaration()
            self.declarations()
        # declarations -> Epsilon
        else:
            pass
        
    def declaration(self):
        # declaration -> ID EQ method NEWLINE
        if self.token.type == 'ID':
            print('    declaration start')
            self.take_token('ID')
            self.take_token('EQ')
            self.method()
            self.take_token('NEWLINE')
            print('    declaration ok')
        else:
            self.error('Expected ID token')
            
    def method(self):
        if self.token.type == 'VOLTAGESOURCE':
            self.voltagesource()
        elif self.token.type == 'VOLTAGEPROBE':
            self.voltageprobe()
        elif self.token.type == 'CURRENTSOURCE':
            self.currentsource()
        elif self.token.type == 'CURRENTPROBE':
            self.currentprobe()
        elif self.token.type == 'RESISTOR':
            self.resistor()
        elif self.token.type == 'CAPACITOR':
            self.capacitor()
        elif self.token.type == 'INDUCTOR':
            self.inductor()
        elif self.token.type == 'DIODE':
            self.diode()
            
    def voltagesource(self):
        # voltagesource -> VOLTAGESOURCE RBO optional_num RBC
        if self.token.type == 'VOLTAGESOURCE':
            self.take_token('VOLTAGESOURCE')
            self.take_token('RBO')
            self.optional_num()
            self.take_token('RBC')
            print('      voltagesource method ok')
        else:
            self.error('expected VOLTAGESOURCE token')
            
    def voltageprobe(self):
        # voltageprobe -> VOLTAGREPROBE RBO RBC 
        if self.token.type == 'VOLTAGEPROBE':
            self.take_token('VOLTAGEPROBE')
            self.take_token('RBO')
            self.take_token('RBC')
            print('      voltageprobe method ok')
        else:
            self.error('expected VOLTAGEPROBE token')
    
    def currentsource(self):
        # currentsource -> CURRENTSOURCE RBO optional_num RBC
        if self.token.type == 'CURRENTSOURCE':
            self.take_token('CURRENTSOURCE')
            self.take_token('RBO')
            self.optional_num()
            self.take_token('RBC')
            print('      currentsource method ok')
        else:
            self.error('expected CURRENTSOURCE token')
    
    def currentprobe(self):
        # currentprobe -> CURRENTPROBE RBO RBC
        if self.token.type == 'CURRENTPROBE':
            self.take_token('CURRENTPROBE')
            self.take_token('RBO')
            self.take_token('RBC')
            print('      currentprobe method ok')
        else:
            self.error('expected CURRENTPROBE token')
    
    def resistor(self):
        # resistor -> RESISTOR RBO NUM RBC
        if self.token.type == 'RESISTOR':
            self.take_token('RESISTOR')
            self.take_token('RBO')
            self.num()
            self.take_token('RBC')
            print('      resistor method ok')
        else:
            self.error('expected RESISTOR token')
    
    def capacitor(self):
        # capacitor -> CAPACITOR RBO NUM RBC
        if self.token.type == 'CAPACITOR':
            self.take_token('CAPACITOR')
            self.take_token('RBO')
            self.num()
            self.take_token('RBC')
            print('      capacitor method ok')
        else:
            self.error('expected CAPACITOR token')
    
    def inductor(self):
        # inductor -> INDUCTOR RBO NUM RBC
        if self.token.type == 'INDUCTOR':
            self.take_token('INDUCTOR')
            self.take_token('RBO')
            self.num()
            self.take_token('RBC')
            print('      inductor method ok')
        else:
            self.error('expected INDUCTOR token')
    
    def diode(self):
        # diode -> DIODE named_args RBC
        if self.token.type == 'DIODE':
            print('      diode method start')
            self.take_token('DIODE')
            self.take_token('RBO')
            self.named_args()
            self.take_token('RBC')
            print('      diode method ok')
        else:
            self.error('expected DIODE token')
             
    def optional_num(self):
        # optional_num -> num
        if self.token.type in ['INT', 'DEC', 'SCI']:
            self.num()
        # optional_num -> Epsilon
        else:
            pass
    
    def num(self):
        # num -> 
        if self.token.type == 'INT':
            self.take_token('INT')
        elif self.token.type == 'DEC':
            self.take_token('DEC')
        elif self.token.type == 'SCI':
            self.take_token('SCI')
        else:
            self.error('Expected INT DEC or SCI tokens')
            
    def named_args(self):
        # named_args -> named_arg next_named_arg
        if self.token.type == 'ID':
            print('        named args start')
            self.named_arg()
            self.next_named_arg()
            print('        named args ok')
        # named_args -> Epsilon
        else:
            pass
    
    def named_arg(self):
        # named_arg -> ID EQ NUM
        if self.token.type == 'ID':
            self.take_token('ID')
            self.take_token('EQ')
            self.num()
            print('          named_arg ok')
        else:
            self.error('expected ID token')
    
    def next_named_arg(self):
        # next_named_arg -> COMA named_arg next_named_arg
        if self.token.type == 'COMA':
            self.take_token('COMA')
            self.named_arg()
            self.next_named_arg()
        else:
            pass
            
    def module_separator(self):
        # module_Separator -> NEWLINE empty_lines
        if self.token.type == 'NEWLINE':
            print('  module separator start')
            self.take_token('NEWLINE')
            self.empty_lines()
            print('  module_separator ok')
        else:
            self.error('expected NEWLINE token')
            
    def empty_lines(self):
        # empty_lines -> NEWLINE empty_lines
        if self.token.type == 'NEWLINE':
            self.take_token('NEWLINE')
            self.empty_lines()
        else:
            pass 
            
            
    def links(self):
        # links -> link links
        if self.token.type in ['ID', 'GND']:
            self.link()
            self.links()
        else:
            pass
        
    def link(self):
        # link -> linkable_value LNK linkable_value next_link NEWLINE
        if self.token.type in ['ID', 'GND']:
            print('    link start')
            self.linkable_value()
            self.take_token('LINK')
            self.linkable_value()
            self.next_link()
            self.take_token('NEWLINE')
            print('    link ok')
        else:
            self.error('Expected ID or GND tokens')
    
    def linkable_value(self):
        print('      linkable value start')
        # linkable_value -> GND
        if self.token.type == 'GND':
            self.take_token('GND')
            print('      linkable_value ok')
        # linkable_value -> indexed_value
        elif self.token.type == 'ID':
            self.indexed_value()
            print('      linkable_value ok')
        else: 
            self.error('Expected GND or ID tokens')
            
    def indexed_value(self):
        # indexed_value -> ID SBO INT SBC
        if self.token.type == 'ID':
            self.take_token('ID')
            self.take_token('SBO')
            self.take_token('INT')
            self.take_token('SBC')
        else:
            self.error('Expected ID token')      
    
    def next_link(self):
        # next_link -> LINK linkable_value next_link
        if self.token.type == 'LINK':
            self.take_token('LINK')
            self.linkable_value()
            self.next_link()
        else:
            pass
        
