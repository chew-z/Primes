module Fprimes
! Don't be lazy compile with f2py using check=all option for fortran
! It can save you hours and maybe days of looking for weird errors
! f2py3.6 -c Primes.f90 -m fprimes <-- STUPID
! f2py3.6 --f90flags=-fcheck=all -c Primes.f90 -m fprimes <-- SMART
implicit none
contains

subroutine sieve(is_prime, n_max)
! =====================================================
! Uses the sieve of Eratosthenes to compute a logical
! array of size n_max, where .true. in element i
! indicates that i is a prime.
! =====================================================
    logical, intent(out)  :: is_prime(n_max)
    integer, intent(in)   :: n_max
    integer :: i

    is_prime = .true.
    is_prime(1) = .false.
    do i = 2, int(sqrt(real(n_max)))
        if (is_prime (i)) is_prime (i * i : n_max : i) = .false.
    end do
end subroutine

subroutine logical_to_integer(prime_numbers, is_prime, n_primes, n_max)
! =====================================================
! Translates the logical array from sieve to an array
! of size num_primes of prime numbers.
! =====================================================
    logical, intent(in)     :: is_prime(n_max)
    integer, intent(out)    :: prime_numbers(n_primes)
    integer, intent(in)     :: n_primes
    integer, intent(in)     :: n_max
    integer                 :: i, j

    j = 1
    do i = 1, size(is_prime)
        if (is_prime(i)) then
            prime_numbers(j) = i
            j = j + 1
        end if
    end do
end subroutine

subroutine all_in_one(numbers, n_max, n_p)
! =====================================================
! ALL-IN-ONE
! =====================================================
    integer, intent(out)    :: numbers(n_p)
    integer, intent(in)     :: n_max
    integer, intent(in)     :: n_p

    logical, allocatable  :: is_prime(:)
    integer                 :: i, j, m

    allocate(is_prime(n_max))
    is_prime = .true.
    is_prime(1) = .false.
    m = int(sqrt(real(n_max)))
    do i = 2, m
        if (is_prime(i)) is_prime (i * i : n_max : i) = .false.
    end do

    ! m = 0
    ! do i=1,n_max
    !     if (is_prime(i)) then
    !         m = m + 1
    !     end if
    ! end do

    j = 1
    m = size(is_prime)
    do i = 1, m
        if (is_prime(i)) then
            numbers(j) = i
            j = j + 1
            if (j == m) exit
        end if
    end do
end subroutine

end module Fprimes
