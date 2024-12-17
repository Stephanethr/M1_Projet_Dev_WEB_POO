from rpg_avatar import Avatar
from rpg_heros import Heros
from rpg_monstre import Monstre

def lancer_combat(avatar1:Avatar, avatar2:Avatar):
    if isinstance(avatar1, Heros):
        return combat(avatar1, avatar2)
    else:
        return combat(avatar2, avatar1)

def combat(heros:Heros, monstre:Monstre):
    heros_gagne = False
    #heros.afficher_stats()
    #monstre.afficher_stats()
    #print("=== Début du combat ===")
    while(monstre.est_vivant and heros.est_vivant):

        #heros.afficher_stats()
        #monstre.afficher_stats()
        
        degats_heros = heros.calculer_degats()
        #print(f"\n{heros.name} inflige {degats_heros} dégâts à {monstre.name}")
        
        if monstre.recevoir_degats(degats_heros):
            print(f"{monstre.name} est vaincu!")
            xp_gagne = heros.gagner_experience(monstre.niveau)
            print(f"{heros.name} gagne {xp_gagne} points d'expérience")
            heros_gagne = True
            break
        else:
            degats_monstre = monstre.calculer_degats()
            if not heros.recevoir_degats(degats_monstre):
                pass
                #print(f"{monstre.name} inflige {degats_monstre} dégâts à {heros.name}")
            else:
                print(f"{heros.name} est mort!")
                break
    
    #print("\n=== État après le combat ===")
    #heros.afficher_stats()
    #monstre.afficher_stats()
    heros.dissiper_effets_temporaires()
    return heros_gagne