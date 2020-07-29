
from application.db.standup import Standup, Shutdown

Shutdown()()
s = Standup()
s()
s.create_test_entities()

