import sys
from django.core.management.base import BaseCommand
from optparse import make_option


class Command(BaseCommand):
    help = "Provides feedback about the current Haystack setup."
    option_list = BaseCommand.option_list + (
        make_option('--force', '-f', action="store_true", dest='force', default=False,
                    help='Force operation'),
    )

    
    def handle(self, *args, **options):
        """Provides feedback about the current Haystack setup."""
        # Cause the default site to load.
        from haystack import site
        if not options['force']:
            print
            print "WARNING: This will irreparably remove EVERYTHING from your search index."
            print "Your choices after this are to restore from backups or rebuild via the `reindex` command."
            
            yes_or_no = raw_input("Are you sure you wish to continue? [y/N] ")
            print
            
            if not yes_or_no.lower().startswith('y'):
                print "No action taken."
                sys.exit()
            
            print "Removing all documents from your index because you said so."
        
        from haystack import backend
        sb = backend.SearchBackend()
        sb.clear()
        
        print "All documents removed."
