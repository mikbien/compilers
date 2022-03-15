class MyParser:

    ##### Parser header #####
    def __init__(self, scanner):
        print('**** PARSER ****\n\n')
        self.next_token = scanner.next_token
        self.token = self.next_token()

    def take_token(self, token_type):
        if self.token.type != token_type:
            self.error("Unexpected token: %s" % token_type)
        if token_type != 'END':
            self.token = self.next_token()

    def error(self,msg):
        raise RuntimeError('Parser error, %s' % msg)

    ##### Parser body #####

    # Starting symbol
    def start(self):
        # program
        self.program()

    def program(self):
        # program -> new_lines BEGIN NEWLINE declarations NEWLINE links END new_lines
        if self.token.type in ['NEWLINE', 'BEGIN']:
            self.new_lines()
            self.take_token('BEGIN')
            self.take_token('NEWLINE')
            self.declarations()
            self.take_token('NEWLINE')
            self.links()
            self.take_token('END')
        # if self.token.type == 'PRINT' or self.token.type == 'ID' or self.token.type == 'IF':
        #     self.statement()
        #     self.program()
        # program -> eps
        else:
            self.error('Expected a BEGIN statement')
    
        
    def new_lines(self):
        if self.token.type == 'NEWLINE':
            self.take_token('NEWLINE')
            self.new_lines()
        else:
            pass
            
    
    def declarations(self):
        # declarations -> new_lines declaration declarations        
        if self.token.type in ['NEWLINE', 'ID']:
            self.new_lines()
            self.declaration()
            self.declarations()
        # declarations -> Epsilon
        else:
            pass
        
    def declaration(self):
        # declaration -> ID EQ method NEW_LINE
        if self.token.type == 'ID':
            self.take_token('ID')
            self.take_token('EQ')
            self.method()
            self.take_token('NEWLINE')
            print('declaration ok')
        else:
            self.error('Epsilon not allowed')
            
    def method(self):
        if self.token.type == 'VOLTAGESOURCE':
            self.voltagesource()
        elif self.token.type == 'VOLTAGREPROBE':
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
            print('voltagesource method ok')
        else:
            self.error('Epsilon not allowed')
            
    def voltageprobe(self):
        # voltageprobe -> VOLTAGREPROBE RBO RBC 
        if self.token.type == 'VOLTAGEPROBE':
            self.take_token('VOLTAGEPROBE')
            self.take_token('RBO')
            self.take_token('RBC')
            print('voltageprobe method ok')
        else:
            self.error('Epsilon not allowed')
    
    def currentsource(self):
        # currentsource -> CURRENTSOURCE RBO optional_num RBC
        if self.token.type == 'CURRENTSOURCE':
            self.take_token('CURRENTSOURCE')
            self.take_token('RBO')
            self.optional_num()
            self.take_token('RBC')
            print('currentsource method ok')
        else:
            self.error('Epsilon not allowed')
    
    def currentprobe(self):
        # currentprobe -> CURRENTPROBE RBO RBC
        if self.token.type == 'CURRENTPROBE':
            self.take_token('CURRENTPROBE')
            self.take_token('RBO')
            self.take_token('RBC')
            print('currentprobe method ok')
        else:
            self.error('Epsilon not allowed')
    
    def resistor(self):
        # resistor -> RESISTOR RBO NUM RBC
        if self.token.type == 'RESISTOR':
            self.take_token('RESISTOR')
            self.take_token('RBO')
            self.num()
            self.take_token('RBC')
            print('resistor method ok')
        else:
            self.error('Epsilon not allowed')
    
    def capacitor(self):
        # capacitor -> CAPACITOR RBO NUM RBC
        if self.token.type == 'CAPACITOR':
            self.take_token('CAPACITOR')
            self.take_token('RBO')
            self.num()
            self.take_token('RBC')
            print('capacitor method ok')
        else:
            self.error('Epsilon not allowed')
    
    def inductor(self):
        # inductor -> INDUCTOR RBO NUM RBC
        if self.token.type == 'INDUCTOR':
            self.take_token('INDUCTOR')
            self.take_token('RBO')
            self.num()
            self.take_token('RBC')
            print('inductor method ok')
        else:
            self.error('Epsilon not allowed')
    
    def diode(self):
        # diode -> DIODE named_args RBC
        if self.token.type == 'DIODE':
            self.take_token('DIODE')
            self.take_token('RBO')
            self.named_args()
            self.take_token('RBC')
            print('diode method ok')
        else:
            self.error('Epsilon not allowed')
             
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
            self.error('Epsilon not allowed')
            
    def named_args(self):
        # named_args -> named_arg next_named_arg
        if self.token.type == 'ID':
            self.named_arg()
            self.next_named_arg()
        # named_args -> Epsilon
        else:
            pass
    
    def named_arg(self):
        # named_arg -> ID EQ NUM
        if self.token.type == 'ID':
            self.take_token('ID')
            self.take_token('EQ')
            self.num()
            print('named_arg ok')
        else:
            self.error('Epsilon not allowed')
    
    def next_named_arg(self):
        # next_named_arg -> COMA named_arg next_named_arg
        if self.token.type == 'COMA':
            self.take_token('COMA')
            self.named_arg()
            self.next_named_arg()
        else:
            pass
            
    def links(self):
        # links -> new_lines link links
        if self.token.type in ['NEWLINE', 'ID']:
            self.new_lines()
            self.link()
            self.links()
        else:
            pass
        
    def link(self):
        # link -> linkable_value LNK linkable_value next_link NEWLINE
        if self.token.type == 'ID':
            self.linkable_value()
            self.take_token('LINK')
            self.linkable_value()
            self.next_link()
            self.take_token('NEWLINE')
            print('link ok')
        else:
            self.error('Epsilon not allowed')
    
    def linkable_value(self):
        # linkable_value -> GND
        if self.token.type == 'GND':
            self.take_token('GND')
            print('linkable_value ok')
        # linkable_value -> indexed_value
        elif self.token.type == 'ID':
            self.indexed_value()
            print('linkable_value ok')
        else: 
            self.error('Epsilon not allowed')
            
    def indexed_value(self):
        # indexed_value -> ID SBO INT SBC
        if self.token.type == 'ID':
            self.take_token('ID')
            self.take_token('SBO')
            self.take_token('INT')
            self.take_token('SBC')
            print('indexed value ok')
        else:
            self.error('Epsilon not allowed')      
    
    def next_link(self):
        # next_link -> LINK linkable_value next_link
        if self.token.type == 'LINK':
            self.take_token('LINK')
            self.linkable_value()
            self.next_link()
        else:
            pass
        
