#!/usr/bin/env ruby
# BULLS
# Kanwei Li, 2010

# Make sure input file exists and read from it
filename = ARGV[0]
# filename = "in1"
unless filename && File.exist?(filename)
  puts "error: must specify a valid input file"
  exit
end
input = File.open(filename).readlines

$graph = {}
$costs = {}

input.each do |line|
  break if line.strip.empty?
  move = line.split(/\s+/)
  if $graph[move[1]] && $graph[move[1]][move[2]]
    next if $costs[$graph[move[1]][move[2]]] < move[3].to_i
  end
  ($graph[move[1]] ||= {})[move[2]] = move[0]
  $costs[move[0]] = move[3].to_i
end

total_cost = $costs.inject(0) { |sum, m| sum += m[1] }
$best_cost, $best_cand = total_cost, $costs.keys
$sink = $graph.keys[0]

def collapse(graph, nodes)
  g = {}
  graph.each { |src, d_m|
    d_m.each { |dest, machine|
      if !nodes.include?(src) && !nodes.include?(dest)
        (g[src] ||= {})[dest] = machine
      elsif nodes.include?(src) && !nodes.include?(dest)
        if g[$sink] && g[$sink][dest]
          g[$sink][dest] = machine if $costs[ graph[src][dest] ] < $costs[ g[$sink][dest] ]
        else
          (g[$sink] ||= {})[dest] = machine
        end
      elsif !nodes.include?(src) && nodes.include?(dest)
        if g[src] && g[src][$sink]
          g[src][$sink] = machine if $costs[ graph[src][dest] ] < $costs[ g[src][$sink] ]
        else
          (g[src] ||= {})[$sink] = machine
        end
      end
    }
  }
  g
end

def search(graph, curr, cost, used, path)
  return if cost >= $best_cost
  if curr == $sink && !path.empty?
    g = collapse(graph, path.uniq)
    if g.length <= 1
      $best_cost, $best_cand = cost, used.uniq if cost < $best_cost
      return
    end
    search(g, $sink, cost, used, [])
  else
    graph[curr].each { |node, machine|
      next if path.include?(node) && node != $sink
      search(graph, node, cost + $costs[machine], used + [machine], path + [curr])
    }
  end
end

search($graph, $sink, 0, [], [])

good_machines = $best_cand.collect { |m| m[1..-1].to_i }.sort.join(" ")
puts "#{$best_cost}\n#{good_machines}\n"
