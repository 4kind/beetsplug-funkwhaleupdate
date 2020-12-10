# beetsplug-funkwahleupdate
This Beets Plugin imports/refreshes items in Funkwhle that are imported by deezer. 

## Current features:
* create/refresh albums/items when `beets import` is executed 

## Configuration
```yaml
funkwahleupdate:
    host: localhost
    port: 5000
    token <app-token>
    library_name: <library-name>
```

## Install
1. `pip install git+https://github.com/4kind/beetsplug-funkwhale@master`
2. enable plugin `funkwhaleupdate` in beets config
3. import items with `beet import`

## Uninstall
`pip uninstall beets-funkwhaleupdate`