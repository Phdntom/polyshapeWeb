



import PolyShape as ps





if __name__ == '__main__':

    N = 10

    omino = ps.PolyShape("polyomino", N)
    print( omino )
    print( omino.get_count() )

    plet = ps.PolyShape("polyplet", N)
    print( plet )
    print( plet.get_count() )

    yhex = ps.PolyShape("polyhex", N)
    print( yhex )
    print( yhex.get_count() )

    if N > 5:
        iamond = ps.PolyShape("polyiamond", N-4)
        print( iamond )
        print( iamond.get_count() )

        iamond = ps.PolyShape("polyiamond", N-3)
        print( iamond )
        print( iamond.get_count() )

        iamond = ps.PolyShape("polyiamond", N-2)
        print( iamond )
        print( iamond.get_count() )

        iamond = ps.PolyShape("polyiamond", N-1)
        print( iamond )
        print( iamond.get_count() )

    iamond = ps.PolyShape("polyiamond", N)
    print( iamond )
    print( iamond.get_count() )



    print("hola")



