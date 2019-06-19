import dork.saveload
from tests.utils import has_many, is_a

def testload():
    """load should grab the data and parse it without further input
    """
    test = dork.saveload.load("./dork/yaml/dork.yml")
    assert "Items" in test, \
        "Saveload.load method failed."
    
    test = dork.saveload.load("Junk")
    assert "Try again" in test, \
        "Saveload.load method could not find proper save data."

def testsave():
    """save will take the current data and save it to a yml file
    """
    test = dork.saveload.save()
    assert "1" in test, \
        "Saveload.save method failed. Why?"

def testplayer(run):
    testvar1 = {'Items':{'holding':"Sword"}}
    testvar2 = 'Items'
    testvar3 = 'holding'

    out, err = run(dork.saveload.player, testvar1, testvar2, testvar3)
    assert "Sword" in out, \
        "Failed to run the saveload.player method: {err}".format(err=err)
    
    testvar1 = {'Position':{'location':"Cliff"}}
    testvar2 = 'Position'
    testvar3 = 'location'

    out, err = run(dork.saveload.player, testvar1, testvar2, testvar3)
    assert "Cliff" in out, \
        "Failed to run the saveload.player method: {err}".format(err=err)
    
    testvar1 = {'HP':{'current':95}}
    testvar2 = 'HP'
    testvar3 = 'current'

    out, err = run(dork.saveload.player, testvar1, testvar2, testvar3)
    assert "95" in out, \
        "Failed to run the saveload.player method: {err}".format(err=err)

    testvar1 = {'HP':{'current':None}}
    testvar2 = 'HP'
    testvar3 = 'current'

    out, err = run(dork.saveload.player, testvar1, testvar2, testvar3)
    assert "There is" in out, \
        "Failed to run the saveload.player method: {err}".format(err=err)

    testvar1 = {'HP':{'current':95}}
    testvar2 = 'HP'
    testvar3 = 'poop'

    out, err = run(dork.saveload.player, testvar1, testvar2, testvar3)
    assert "." in out, \
        "Failed to run the saveload.player method: {err}".format(err=err)

    testvar1 = {'Happiness':{'level':12}}
    testvar2 = 'Happiness'
    testvar3 = 'level'

    out, err = run(dork.saveload.player, testvar1, testvar2, testvar3)
    assert "Player's" in out, \
        "Failed to run the saveload.player method: {err}".format(err=err)

def testitem(run):
    testvar1 = {'Cliff':{'holds':None}}
    testvar2 = 'Cliff'
    testvar3 = 'holds'

    out, err = run(dork.saveload.item, testvar1, testvar2, testvar3)
    assert "Cliff" in out, \
        "Failed to run the saveload.item method: {err}".format(err=err)
    
    testvar1 = {'Cliff':{'holds':"Sword"}}

    out, err = run(dork.saveload.item, testvar1, testvar2, testvar3)
    assert "Sword" in out, \
        "Failed to run the saveload.item method: {err}".format(err=err)

    testvar3 = 'poop'

    out, err = run(dork.saveload.item, testvar1, testvar2, testvar3)
    assert "poop" in out, \
        "Failed to run the saveload.item method: {err}".format(err=err)


def testpath(run):
    out, err = run(dork.saveload.path, "Junk", 2, "Stuff")
    assert "does not have" in out, \
        "Failed to run the saveload.path method: {err}".format(err=err)

    testvar1 = {'Cliff':{'east':None}}
    testvar2 = 'Cliff'
    testvar3 = 'east'

    out, err = run(dork.saveload.path, testvar1, testvar2, testvar3)
    assert "Cliff" in out, \
        "Failed to run the saveload.path method: {err}".format(err=err)

    testvar1 = {'Cliff':{'east':'Graveyard'}}

    out, err = run(dork.saveload.path, testvar1, testvar2, testvar3)
    assert "Cliff" in out, \
        "Failed to run the saveload.path method: {err}".format(err=err)

    testvar3 = 'lol'

    out, err = run(dork.saveload.path, testvar1, testvar2, testvar3)
    assert "Cliff" in out, \
        "Failed to run the saveload.path method: {err}".format(err=err)

    testvar1 = {'Cliff':{'east':'Graveyard'},'Graveyard':{'west':'Cliff'}}
    testvar2 = 'Cliff'
    testvar3 = 'east'

    out, err = run(dork.saveload.path, testvar1, testvar2, testvar3)
    assert "Cliff" in out, \
        "Failed to run the saveload.path method: {err}".format(err=err)

def testmain(run):
    out, err = run(dork.saveload.main)
    assert "Checking" in out, \
        "Failed to run the saveload.main method: {err}".format(err=err)