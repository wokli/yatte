# Yatte
## Yet Another *Toy* Template Engine

### Usage:
    from yatte import Template as t
    tmpl = t('''{% each list %}
        {% if _ < 3 %}
            sup {{ _ }}
        {% end %}
    {% end %}''')
    
    print tmpl.render({'list':range(5)})
    
 Output:
 
    sup 0 sup 1 sup 2

### Template syntax:

1. Variable:

    ```{{ var }}```
2. Loop the list:

    ```{% each list %} {{ _ }} {% end %}```
    
    ```_``` represents a single value from the list.

3. Conditional: 
    
    ```{% if var < 5 %} Some text {% end %}```

###Thx to:

 [alexmic](http://alexmic.net)

 [500 lines or less](http://aosabook.org/en/500L/)
