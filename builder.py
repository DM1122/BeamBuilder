import drawlib, veclib, civlib

# mm
thick = 1.27
altitude = 200
track_base = 100
web_sep = 75
fold = 10




# materials dictionary
materials = {
    'matboard':{
        'density': 7.626*10**-4,        # [g/mm^3]
        'tensile': 30,              # tensile strength [MPa]
        'compressive': 6,           # compressive strength [MPa]
        'shear': 4,                 # shear strenght [MPa]
        'E': 4000,                  # Young's mod [MPa]
        'Mu': 0.2,              # Poisson's ratio
    },

    'glue':{
        'shear': 2        # shear strength [MPa]
    }
}


class section:
    def __init__(self, base, height, position, material):
        self.b = base
        self.h = height
        self.pos = position
        self.mat = material
        
        self.com = [base/2, height/2]
        self.area = base * height
        self.mass = material['density'] * (base * height)
        self.inertia = (base * height**3) / 12
    
    def __str__(self):

        out = 'Section id:{} \n Base:{} \n Height:{} \n Pos:{} \n Material:{} \n CoM:{} \n Area:{} \n Mass:{} \n Inertia:{}'.format(id(self), self.b, self.h, self.pos, self.mat, self.com, self.area, self.mass, self.inertia)

        return out

    def PAT(self, origin):
        '''
        Computes section inertia relative to new origin according to parrallel axis theorem.
        '''

        dy = self.pos[1] - origin[1]
        I = self.inertia + self.mat['density'] * dy**2

        return I
    


class structure:
    def __init__(self, sections):
        self.sections = sections


        self.com = self.calc_com()
        self.top = self.sections[-1].pos[1] + (self.sections[-1].h)/2
        self.com_to_top = self.top - self.com[1]
        self.com_to_bot = 0 - self.com[1]
        self.inertia = self.calc_I()
        self.Q = self.calc_Q()
        self.b = self.calc_b()

    def __str__(self):

        out = 'Structure id:{} \n CoM:{} \n I:{} \n Q:{} \n b:{} \n # Sections: {}'.format(id(self), self.com, self.inertia, self.Q, self.b, len(self.sections)) 

        return out

    def calc_com(self):
        # currently only calculates vertical CoM axis

        net_mass = 0
        net_massx = 0
        for sec in self.sections:
            net_massx += sec.mass * sec.pos[1]
            net_mass += sec.mass
        
        com = [0, (net_massx/net_mass)]

        return com
    
    def calc_I(self):
        
        I_net = 0
        for sec in self.sections:
            I_net += sec.PAT(self.com)

        return I_net
    
    def calc_Q(self):

        A = 2*(thick * self.com[1])
        d = self.com[1]/2
        Q = A * d

        return Q
    
    def calc_b(self):

        b = 2*thick

        return b



def build_struct(altitude=altitude):
    # already ordered from bottom left to top right
    web_L = section(thick, altitude - 3*thick, [-((web_sep/2) + (thick/2)), (altitude-3*thick)/2], materials['matboard'])
    web_R = section(thick, altitude - 3*thick, [((web_sep/2) + thick/2), (altitude-3*thick)/2], materials['matboard'])
    fold_L = section(fold, thick, [-(web_sep/2 + fold/2), altitude - (5/2)*thick], materials['matboard'])
    fold_R = section(fold, thick, [(web_sep/2 + fold/2), altitude - (5/2)*thick], materials['matboard'])
    track_A = section(track_base, thick, [0, altitude - thick/2], materials['matboard'])
    track_B = section(track_base, thick, [0, altitude - (3/2)*thick], materials['matboard'])

    sections = [track_A, track_B, web_L, web_R, fold_L, fold_R]

    # # sort sections according to height
    # heights = []
    # for sec in sections:
    #     heights.append(sec.pos[1])

    # XY = sorted(zip(heights, sections), reverse=False)    # sort in ascending order (does not work)

    # sections = [y for (x,y) in XY]

    struct = structure(sections)

    return struct



if __name__ == '__main__':
    struct = build_struct()
    print(struct)


    # #region draw
    # drawlib.setup()
    # drawlib.draw_axes()

    # for sec in struct.sections:
    #     drawlib.draw_section(sec)
    
    # drawlib.draw_com(struct)
    # drawlib.hide()
    # #endregion
    






    input("Press Enter to continue...")
