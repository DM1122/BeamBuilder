import drawlib, veclib

thick = 0.00127
altitude = 0.2
track_base = 0.1
web_sep = 0.075
fold = 0.01

#Load case info
V_max_factor = 1            # *P
M_max_factor = 0.1899       # *P


# materials dictionary
materials = {
    'matboard':{
        'density': 800,         # [kg/m^3]
        'tensile': 30000000,    # tensile strength [Pa]
        'compressive': 6000000, # compressive strength [Pa]
        'shear': 4000000,       # shear strenght [Pa]
        'E': 4000000000,        # Young's mod [Pa]
        'Mu': 0.2,              # Poisson's ratio
    },

    'glue':{
        'shear': 2000000        # shear strength [Pa]
    }
}


class section:
    # currently only supports 2D geometry sections

    def __init__(self, base, height, position, material):
        self.b = base
        self.h = height
        self.pos = position
        self.mat = material
        
        self.com = [base/2, height/2]
        self.area = base * height
        self.mass = material['density'] * (base * height)
        self.inertia = (base * height**3) / 12
    

    def PAT(self, origin):
        '''
        Computes section inertia relative to new origin according to parrallel axis theorem.
        '''

        dy = self.pos[1] - origin[1]
        I = self.inertia + self.mat['density'] * dy**2

        return I
    

class cross_section:

    def __init__(self, sections):
        self.sections = sections

        self.com = self.calcCoM()
        self.inertia = self.calcI()
    
    def calcCoM(self):
        # currently only calculates vertical CoM axis

        net_mass = 0
        net_massx = 0
        for sec in self.sections:
            net_massx += sec.mass * sec.pos[1]
            net_mass += sec.mass
        
        com = [0, (net_massx/net_mass)]

        return com
    
    def calcI(self):
        
        I_net = 0
        for sec in self.sections:
            I_net += sec.PAT(self.com)

        return I_net
        

def build_struct(altitude=altitude):
    track_A = section(track_base, thick, [0, altitude - thick/2], materials['matboard'])
    track_B = section(track_base, thick, [0, altitude - (3/2)*thick], materials['matboard'])
    web_L = section(thick, altitude - 3*thick, [-((web_sep/2) + (thick/2)), (altitude-3*thick)/2], materials['matboard'])
    web_R = section(thick, altitude - 3*thick, [((web_sep/2) + thick/2), (altitude-3*thick)/2], materials['matboard'])
    fold_L = section(fold, thick, [-(web_sep/2 + fold/2), altitude - (5/2)*thick], materials['matboard'])
    fold_R = section(fold, thick, [(web_sep/2 + fold/2), altitude - (5/2)*thick], materials['matboard'])

    sections = [track_A, track_B, web_L, web_R, fold_L, fold_R]         # temp storage soltion
    struct = cross_section(sections)

    return struct


if __name__ == '__main__':
    struct = build_struct()


    #region draw
    drawlib.setup()
    drawlib.draw_axes()

    for sec in struct.sections:
        drawlib.draw_section(sec)
    
    drawlib.hide()
    #endregion
    

    # calculations

    P = flexForce(matboard['tensile'], struct.inertia, altitude, M_max_factor)
    print(P)




    input("Press Enter to continue...")
