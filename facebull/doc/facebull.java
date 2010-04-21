package ynamara.fbpuzzle;
import java.io.*;
import java.util.*;

public class facebull {

    static class Index {
        Map<String, Integer> map;
        List<String> list;
        Index() {
            map = new HashMap<String, Integer>();
            list = new ArrayList<String>();
        }
        int indexOf(String s) {
            Integer ii = map.get(s);
            if (ii == null) {
                map.put(s, ii = map.size());
                list.add(s);
            }
            return ii;
        }
        String at(int i) {
            return list.get(i);
        }
    }

    Index compoundsIndex = new Index();
    List<Machine> machines = new ArrayList<Machine>();
    int numCompounds;
    int bestCost = Integer.MAX_VALUE;
    BitSet bestSet = null;
    BitSet[] outgoing;
    
    static BitSet copy(BitSet b) {
        BitSet ret = new BitSet();
        ret.or(b);
        return ret;
    }

    static BitSet or(BitSet b1, BitSet b2) {
        BitSet ret = copy(b1);
        ret.or(b2);
        return ret;
    }

    static BitSet set(BitSet b, int index) {
        BitSet ret = copy(b);
        ret.set(index);
        return ret;
    }

    static class Machine {
        int label;
        int src, dst;
        int cost;
        Machine(int label, int src, int dst, int w) {
            this.label = label;
            this.src = src;
            this.dst = dst;
            this.cost = w;
        }
        public String toString() {
            return label + " " + src + " " + dst + " " + cost;
        }
    }

    static Integer[] asArray(BitSet set) {
        Integer[] ret = new Integer[set.cardinality()];
        for (int i = 0, v = set.nextSetBit(0); v >= 0; v = set.nextSetBit(v + 1)) {
            ret[i++] = v;
        }
        return ret;
    }

    String toStringMachines(BitSet set) {
        BitSet labels = new BitSet();
        for (int i : asArray(set)) {
            labels.set(machines.get(i).label);
        }
        return labels.toString().replaceAll("[^0-9 ]", "");     
    }

    Comparator<Integer> weightComparator = new Comparator<Integer>() {
        public int compare(Integer m1, Integer m2) {
            return machines.get(m1).cost - machines.get(m2).cost;
        }
    };
    
    static Integer[] sortedBy(BitSet set, Comparator<Integer> comparator) {
        Integer[] o = asArray(set);
        Arrays.sort(o, comparator);
        return o;
    }
    
    void search(int current, BitSet loopable, BitSet reached, BitSet used, int cost,
            BitSet path) {
        if (cost >= bestCost) {
            return;
        }
        for (int mIndex: asArray(outgoing[current])) {
            if (used.get(mIndex)) {
                continue;
            }
            Machine m = machines.get(mIndex);
            if (loopable.get(m.dst)) {
                addCycle(or(loopable,path), set(reached,m.dst), set(used,mIndex),
                    cost + m.cost);
            } else if (!reached.get(m.dst)) {
                search(m.dst, loopable, set(reached,m.dst), set(used,mIndex),
                    cost + m.cost, set(path,m.dst));
            }
        }
    } // end of search
                
    void addCycle(BitSet loopable, BitSet reached, BitSet used, int cost) {
        if (reached.cardinality() == numCompounds) {
            if (cost < bestCost) {
                bestCost = cost;
                bestSet = copy(used);
            }
            return;
        }
        Integer[] startPoints = asArray(loopable);
        LinkedList<BitSet> queue = new LinkedList<BitSet>();
        for (int start: startPoints) {
            search(start, loopable, reached, used, cost, new BitSet());
            queue.add(copy(outgoing[start]));
            outgoing[start].clear();
        }
        for (int start: startPoints) {
            outgoing[start].or(queue.remove());
        }
    } // end of addCycle
    
    void solve(Scanner in) {
        while (in.hasNext()) {
            int label = Integer.parseInt(in.next().substring(1));
            int src = compoundsIndex.indexOf(in.next());
            int dst = compoundsIndex.indexOf(in.next());
            int cost = in.nextInt();
            machines.add(new Machine(label, src, dst, cost));
        }
        numCompounds = compoundsIndex.map.size();
        BitSet used = new BitSet();
        used.set(0, machines.size());
        outgoing = new BitSet[numCompounds];
        for (Machine m: machines) {
            BitSet out = outgoing[m.src];
            if (out == null) {
                outgoing[m.src] = out = new BitSet();
            }
            out.set(machines.indexOf(m));
        }
        BitSet compounds = new BitSet();
        compounds.set(0);
        addCycle(compounds, new BitSet(), new BitSet(), 0);
        System.out.println(bestCost);
        System.out.println(toStringMachines(bestSet));
    }

    public static void main(String[] args) throws Exception {
        new facebull().solve(new Scanner(new File(args[0])));
    }
}
