import fitz      # = PyMuPDF


g_toc = []

#doc = fitz.open(r"C:\mybook\Dropbox\books\hw\intellinuxgraphics.org\010_kbl_-_2016-2017\intel-gfx-prm-osrc-kbl-vol02c-commandreference-registers-part1.pdf")
doc = fitz.open(r"C:\mybook\Dropbox\books\hw\intellinuxgraphics.org\010_kbl_-_2016-2017\intel-gfx-prm-osrc-kbl-vol12-display.pdf")

def do_overview():
    toc = doc.getToC()                               # get current table of contents
    for t in toc:
        print(t)

    page = doc.loadPage(2)
    print("page content: {}".format(page))
    links = page.getLinks()
    print("links: {}".format(links))

    for ln in links:
        if ln["kind"] == fitz.LINK_GOTO:
            print("Jump to page", ln["page"] + 1, ln)
        elif ln["kind"] in (fitz.LINK_GOTOR, fitz.LINK_LAUNCH):
            print("Open or launch file", ln["file"])
        elif ln["kind"] == fitz.LINK_URI:
            print("Open URI", ln["uri"])


    tt = page.getText(output='text')
    td = page.getText(output='dict')

    print(tt)
    print(td['blocks'][0])
    for i in td['blocks']:
        if i['type'] == 0:
            print("type is {}, length: {} and {}".format(i['type'], len(i['lines']), i['bbox']))
            if len(i['lines']) == 3:
                print("lens:{}".format(i['lines'][0]))
                print("lens:{}".format(i['lines'][1]))
                print("lens:{}".format(i['lines'][2]))

                label = i['lines'][0]['spans'][0]['text']
                pos = i['lines'][0]['bbox']
                print(label, pos)

    '''
    type is 0, length: 3 and [54.0, 712.4681396484375, 473.59503173828125, 725.9760131835938]
    lens:{'dir': (1.0, 0.0), 'spans': [{'font': 'Segoe UI,Bold', 'size': 9.960000038146973, 'text': 'Aggregate Perf Counter A9 Upper DWord ', 'flags': 16}], 'wmode': 0, 'bbox': (54.0, 712.4681396484375, 252.87896728515625, 725.7157592773438)}
    lens:{'dir': (1.0, 0.0), 'spans': [{'font': 'Segoe UI,Bold', 'size': 9.960000038146973, 'text': '............................................................................... ', 'flags': 16}], 'wmode': 0, 'bbox': (250.85000610351562, 712.4681396484375, 462.178955078125, 725.7157592773438)}
    lens:{'dir': (1.0, 0.0), 'spans': [{'font': 'Segoe UI,Bold', 'size': 9.960000038146973, 'text': '33', 'flags': 16}, {'font': 'Calibri', 'size': 11.039999961853027, 'text': ' ', 'flags': 0}], 'wmode': 0, 'bbox': (459.54998779296875, 712.4681396484375, 473.59503173828125, 725.9760131835938)}
    
    '''

    print("hello----------------------------------")
    items = get_item(page)
    for i in items:
        print(i['label'], i['pos'])

    hylinks = get_links(page)
    for i in hylinks:
        print(i['page'], i['pos'])


    for i in hylinks:
        for j in items:
            # if i['pos'].intersect(j['pos']):
            #    print("True: ", j['label'],i['page'])
            if match(i['pos'], j['pos']):
                print("compare: ", j['pos'][0], i['page'], i['pos'], j['label'], j['pos'], )
                break

#print(td['blocks'])
#doc.setToC(toc)
#doc.save(doc.name, incremental=True)

def get_links(page):
    items = []

    links = page.getLinks()

    for ln in links:
        if ln["kind"] == fitz.LINK_GOTO:
            # print("Jump to page", ln["page"] + 1, ln)
            pass
            items.append({'page': ln["page"] + 1, 'pos': ln["from"]})
        elif ln["kind"] in (fitz.LINK_GOTOR, fitz.LINK_LAUNCH):
            pass
            #print("Open or launch file", ln["file"])
        elif ln["kind"] == fitz.LINK_URI:
            pass
            #print("Open URI", ln["uri"])

    return items

def get_item(page):
    item = []

    td = page.getText(output='dict')
    for i in td['blocks']:
        if i['type'] == 0 and len(i['lines']) == 3:
            label = i['lines'][0]['spans'][0]['text']
            pos = i['lines'][0]['bbox']
            print(label, pos)

            item.append({'label': label, 'pos': pos})


    return item




def match(rect1, rect2):
    r = fitz.Rect(rect2[0], rect2[1], rect2[2], rect2[3])
    #b = rect1.contains(r)  # doesn't work
    b = rect1.intersects(r)
    return b


def update_level():
    print(g_toc)
    print('--update--')
    l = [r[0] for r in g_toc]
    print(l)
    print("---end ---")
    pass


def gen_toc(page):
    items = get_item(page)
    # for i in items:
    #     print(i['label'], i['pos'])

    hylinks = get_links(page)
    # for i in hylinks:
    #     print(i['page'], i['pos'])

    for i in hylinks:
        for j in items:
            # if i['pos'].intersect(j['pos']):
            #    print("True: ", j['label'],i['page'])
            if match(i['pos'], j['pos']):
                print("compare: ", j['pos'][0], i['page'], i['pos'], j['label'], j['pos'], )
                g_toc.append([int(j['pos'][0]), j['label'], i['page']])
                break


def rect_is_match_test():
    r1_link = fitz.Rect(51.75, 133.42999267578125, 473.25, 152.72998046875)
    r2_text = fitz.Rect(54.0, 133.3921661376953, 192.24896240234375, 146.63973999023438)

    print(r1_link.intersects(r2_text))


#do_overview()
page = doc.loadPage(2)
gen_toc(page)
for i in g_toc:
    print(i)

update_level()




