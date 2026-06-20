import { Star, StarOff, Trash2 } from 'lucide-react';
import { SavedQuery } from '../types';

interface SavedQueriesSidebarProps {
  savedQueries: SavedQuery[];
  onLoadQuery: (question: string) => void;
  onDeleteQuery: (id: string) => void;
  onToggleFavorite: (id: string) => void;
}

export function SavedQueriesSidebar({ savedQueries, onLoadQuery, onDeleteQuery, onToggleFavorite }: SavedQueriesSidebarProps) {
  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-gray-900 dark:text-gray-100">
            Saved Queries
          </h3>
        </div>
        {savedQueries.length === 0 ? (
          <div className="text-sm text-gray-500 dark:text-gray-400">
            No saved queries yet!
          </div>
        ) : (
          <div className="space-y-2">
            {savedQueries
              .sort((a, b) => {
                if (a.is_favorite && !b.is_favorite) return -1;
                if (!a.is_favorite && b.is_favorite) return 1;
                return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
              })
              .map((query) => (
                <div
                  key={query.id}
                  className="flex items-center justify-between p-2 rounded-lg bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer"
                  onClick={() => onLoadQuery(query.natural_language_query)}
                >
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate text-gray-900 dark:text-gray-100">
                      {query.name}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                      {query.natural_language_query}
                    </p>
                  </div>
                  <div className="flex items-center gap-1">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onToggleFavorite(query.id);
                      }}
                      className="p-1 hover:text-yellow-500"
                    >
                      {query.is_favorite ? (
                        <Star size={14} className="text-yellow-500" />
                      ) : (
                        <StarOff size={14} />
                      )}
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDeleteQuery(query.id);
                      }}
                      className="p-1 hover:text-red-500"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </div>
              ))}
          </div>
        )}
      </div>
    </div>
  );
}
