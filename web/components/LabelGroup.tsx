import { useState } from 'react';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import { ChevronRight } from 'lucide-react';

interface Label {
  text: string;
  count: number;
  color: string;
}

//example, should come from API, depending of the type we
// should assing a color, eg: papger bg-emeral-400
// I just used the most similar colors from the 
// original neo4j dashbord

const nodeLabels: Label[] = [
  { text: '*', count: 31, color: 'bg-gray-300' },
  { text: 'Model', count: 4, color: 'bg-gray-300' },
  { text: 'Dataset', count: 4, color: 'bg-gray-300' },
  { text: 'Accuracy', count: 1, color: 'bg-gray-300' },
  { text: 'Author', count: 9, color: 'bg-blue-400' },
  { text: 'Code', count: 1, color: 'bg-gray-300' },
  { text: 'Paper', count: 2, color: 'bg-emerald-400' },
  { text: 'Concept', count: 9, color: 'bg-pink-200' },
  { text: 'Field', count: 1, color: 'bg-amber-300' },
];

const relationshipTypes: Label[] = [
  { text: '*', count: 43, color: 'bg-gray-300' },
  { text: 'PERFORMS_ON', count: 1, color: 'bg-gray-300' },
  { text: 'FINE_TUNES_ON', count: 1, color: 'bg-gray-300' },
  { text: 'TRAINS_ON', count: 1, color: 'bg-gray-300' },
  { text: 'TRANSFER_LEARNING_ON', count: 1, color: 'bg-gray-300' },
  { text: 'ACHIEVES', count: 1, color: 'bg-gray-300' },
  { text: 'AUTHORED', count: 1, color: 'bg-gray-300' },
];

// update later to receive nodes and labels as parameters
export function LabelGroup() {
  const [isVisible, setIsVisible] = useState(true);

  return (
    <Card className={`${isVisible ? 'p-6 max-w-xl' : 'p-1 max-w-xs' } bg-zinc-950 text-white`}>
      <div 
        className="flex items-center gap-2 mb-2 cursor-pointer"
        onClick={() => setIsVisible(!isVisible)}
      >
        <h2 className="text-2xl font-semibold">{isVisible ? "Overview" : ""}</h2>
        <ChevronRight className={`transform transition-transform ${isVisible ? 'rotate-90' : ''}`} />
      </div>

      {isVisible && (
        <div className="space-y-8">
          <div>
            <h3 className="text-xl mb-4">Node labels</h3>
            <div className="flex flex-wrap gap-2">
              {nodeLabels.map((label) => (
                <Badge
                  key={`${label.text}-${label.count}`}
                  className={`${label.color} hover:${label.color} text-zinc-900 px-3 py-1 text-sm font-medium`}
                >
                  {label.text} ({label.count})
                </Badge>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-xl mb-4">Relationship types</h3>
            <div className="flex flex-wrap gap-2">
              {relationshipTypes.map((label) => (
                <Badge
                  key={`${label.text}-${label.count}`}
                  className="bg-gray-300 hover:bg-gray-300 text-zinc-900 px-3 py-1 text-sm font-medium"
                >
                  {label.text} ({label.count})
                </Badge>
              ))}
            </div>
          </div>
        </div>
      )}
    </Card>
  );
}