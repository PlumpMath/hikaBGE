def transformCoord(vect,system1,system2):
    """Transforma un vector de un sistema de coordenadas a otro
    vect=vect3d
    system1, system2 = objects"""
    m1=system1.worldOrientation.transposed()
    m2=system2.worldOrientation
    p=m1*m2
    return(p*vect)