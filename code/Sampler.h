#ifndef DNest4_Sampler
#define DNest4_Sampler

#include <vector>
#include <thread>
#include <ostream>
#include <istream>
#include "LikelihoodType.h"
#include "Options.h"
#include "Level.h"
#include "RNG.h"
#include "Barrier.h"

namespace DNest4
{

template<class ModelType>
class Sampler
{
	private:
		// Whether to save anything to disk or not
		// Use 'true' for standard mode
		bool save_to_disk;

		// Threads and barrier
		std::vector<std::thread*> threads;
		Barrier* barrier;

		// Number of threads and compression
		unsigned int num_threads;
		double compression;

		// Options (most useful comment ever)
		Options options;

		// Particles, tiebreaker values, and level assignments
		std::vector<ModelType> particles;
		std::vector<LikelihoodType> log_likelihoods;
		std::vector<unsigned int> level_assignments; // j in the paper

		// Levels
		std::vector<Level> levels;
		std::vector< std::vector<Level> > copies_of_levels;

		// Storage for creating new levels
		std::vector<LikelihoodType> all_above;

		// Random number generators
		std::vector<RNG> rngs;

		// Number of saved particles
		unsigned int count_saves;
		unsigned long long int count_mcmc_steps;

		// Storage for likelihoods above threshold
		std::vector< std::vector<LikelihoodType> > above;

		/* Private methods */
		// Master function to be called from each thread
		void run_thread(unsigned int thread);

		// Do an MCMC step of particle 'which' on thread 'thread'
		void update_particle(unsigned int thread, unsigned int which);

		// Do an MCMC step of the level assignment of particle 'which' on thread
		// 'thread'
		void update_level_assignment(unsigned int thread, unsigned int which);

		// Do MCMC for a while on thread 'thread'
		void mcmc_thread(unsigned int thread);

		// Add new levels, save output files, etc
		void do_bookkeeping();

		// Kill lagging particles
		void kill_lagging_particles();

		// Weighting function
		double log_push(unsigned int which_level) const;

        // Are there enough levels?
        bool enough_levels(const std::vector<Level>& l) const;

		// Functions to do with the output files
		void initialise_output_files() const;
		void save_levels() const;
		void save_particle();

	public:
		Sampler () {};

		// Constructor: Pass in Options object
		Sampler(unsigned int num_threads,
						double compression, const Options& options);

		// Constructor: Pass in Options object and save_to_disk
		Sampler(unsigned int num_threads,
						double compression, const Options& options,
						bool save_to_disk);

		// Set rng seeds, then draw all particles from the prior
		void initialise(unsigned int first_seed);

		// Launch everything
		void run();

		// Increase max_num_saves (allows continuation)
		void increase_max_num_saves(unsigned int increment);

		// GETTERS!!!
		const std::vector<ModelType>& get_particles() const
		{ return particles; }

		const std::vector<LikelihoodType>& get_log_likelihoods() const
		{ return log_likelihoods; }

		const std::vector<unsigned int> get_level_assignments() const
		{ return level_assignments; }

		int size () const { return particles.size(); };
		ModelType* particle (unsigned int i) { return &(particles[i]); };

		const std::vector<Level>& get_levels () const { return levels; };

		void print(std::ostream& out) const;
		void read(std::istream& in);
};

} // namespace DNest4

template<class ModelType>
std::ostream& operator << (std::ostream& out,
								const DNest4::Sampler<ModelType>& s);

#include "SamplerImpl.h"
#endif

