import threading
import time
import queue

txt = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam volutpat condimentum placerat. Sed ultricies, tortor in imperdiet scelerisque, turpis velit tincidunt turpis, id fringilla risus quam non libero. Vivamus blandit imperdiet congue. Nullam scelerisque mattis mauris non viverra. Sed at ex ipsum. Ut sit amet leo id mauris semper bibendum vitae quis tellus. Quisque ut lacus eu odio viverra iaculis pharetra vitae nunc. Ut nisi nunc, efficitur at mattis ac, porttitor sed urna. Etiam sit amet feugiat enim. Integer eu urna eu arcu ultrices auctor. Quisque interdum convallis ex et laoreet. Cras sagittis lacus imperdiet dui molestie, at tempor quam tristique. Suspendisse lobortis fringilla lorem eu vulputate. Sed diam neque, elementum sed cursus ut, tincidunt in magna.
Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent ipsum orci, maximus at urna eu, blandit commodo magna. Suspendisse feugiat quam et tincidunt eleifend. Donec mattis quis sem sed tempus. Phasellus varius arcu quis enim aliquet, sit amet mattis velit luctus. Nunc pretium, libero eu facilisis laoreet, sem elit sodales sem, quis feugiat sem dolor vitae enim. Suspendisse sagittis non arcu vitae auctor. Pellentesque a justo sit amet est pulvinar ultricies vel eget odio. Sed mollis elementum fermentum. Vestibulum at risus quis erat eleifend ornare at eu leo. Suspendisse est nibh, lacinia et nulla id, viverra sagittis quam. Nulla in pharetra neque. Praesent pulvinar elementum erat, hendrerit eleifend mauris dictum et. Nullam eget maximus erat, sollicitudin ultrices nisi. Curabitur sed elementum lacus, quis posuere sem. Phasellus mollis augue metus, vel fringilla dolor lobortis id.
Aenean imperdiet erat ut nunc vulputate, id aliquet lectus tristique. Aenean rutrum eu arcu id efficitur. Nam tempus tellus id dolor aliquam, eget blandit tortor consequat. Pellentesque eget mattis est, ut lacinia est. Aenean fermentum bibendum purus, eget convallis felis sagittis ut. Curabitur quis auctor nisi. Fusce mauris purus, euismod et scelerisque non, vestibulum non mauris. Nulla non orci sit amet magna blandit dignissim vitae ac velit. Nulla dictum quis odio vel bibendum. Nulla faucibus ante id odio accumsan aliquet. Sed laoreet lacinia urna, nec aliquet nulla blandit quis. Curabitur orci risus, convallis vel fringilla rutrum, vulputate at est. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; In et mauris eu mi feugiat elementum vitae sit amet lectus. Sed risus turpis, dictum lobortis nisl non, sollicitudin malesuada nisl. Aenean at dictum libero.
Sed et accumsan quam. Cras vestibulum nisi id ullamcorper bibendum. Maecenas eget iaculis dui. Cras pulvinar velit lectus. Sed mattis est dui, a ultricies erat condimentum non. Nunc ultrices risus est. Maecenas eget fringilla ex.
Nullam ut molestie odio. Curabitur at pharetra dolor. Sed et justo blandit, ullamcorper lacus vitae, blandit ex. Sed non volutpat sem, consectetur pellentesque purus. Vestibulum id velit convallis, molestie nisi vel, placerat ante. Phasellus eget varius ligula, sed scelerisque tortor. Suspendisse ac ante vel est elementum tempus non semper leo. Mauris facilisis, elit at lacinia luctus, orci sem ultricies est, non auctor libero odio at dui. Vivamus sit amet enim non lectus varius lacinia nec at nisl. In molestie interdum nibh. Nulla posuere molestie nisi a eleifend. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Nam bibendum vestibulum tortor, ac luctus sem tempor sed. Integer viverra molestie lacinia.
"""


class Network(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()

    def run(self):
        for t in txt.split():
            time.sleep(1)
            self.queue.put(t + '　')
